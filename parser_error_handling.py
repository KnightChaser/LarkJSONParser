from lark import Lark, UnexpectedInput

json_grammar = """
    ?value: dict
          | list
          | string
          | number
          | "true"
          | "false"
          | "null"

    list: "[" value ("," value)* "]"

    dict: "{" pair ("," pair)* "}"
    pair: string ":" value

    string: ESCAPED_STRING
    number: SIGNED_NUMBER

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
"""

json_parser = Lark(json_grammar, start='value', parser='lalr')

class JsonSyntaxError(SyntaxError):
    def __str__(self):
        context, line, column, problematic_character = self.args
        # Custom error message
        report_string  = f"{'=' * 19} JSON SYNTAX ERROR {'=' * 19}\n"
        report_string += f"Error Type: {self.__class__.__name__}\n"
        report_string += f"{self.label} at line {line}, column {column}.\n"
        report_string += f"Problematic Character: '{problematic_character}'\n"
        report_string += f"{'=' * 24} CONTEXT {'=' * 24}\n"
        report_string += f"{context}"
        report_string += f"{'=' * 57}"
        return report_string

class JsonMissingValue(JsonSyntaxError):
    label = 'Missing Value'

class JsonUnexpectedToken(JsonSyntaxError):
    label = 'Unexpected Token'

class JsonTrailingComma(JsonSyntaxError):
    label = 'Trailing Comma'

class JsonUnmatchedBrace(JsonSyntaxError):
    label = 'Unmatched Brace'


# To classify and handle the syntax errors in a general manner, we manually deduce the type of error
def parse(json_text):
    try:
        j = json_parser.parse(json_text)
    except UnexpectedInput as u:
        # Dynamically deduce the type of error based on the context and token
        context = u.get_context(json_text)
        problematic_character = json_text[u.pos_in_stream]      # Get the problematic character where the parser failed

        if problematic_character == '' or (problematic_character in ['}', ']'] and json_text[u.pos_in_stream - 1] in ['', ' ']):
            raise JsonMissingValue(context, u.line, u.column, problematic_character)
        elif problematic_character in ['}', ']']:
            raise JsonUnmatchedBrace(context, u.line, u.column, problematic_character)
        elif problematic_character == ',' and len(json_text) == u.pos_in_stream + 1:
            raise JsonTrailingComma(context, u.line, u.column, problematic_character)
        else:
            raise JsonUnexpectedToken(context, u.line, u.column, problematic_character)


def test():
    try:
        parse('{"example1": "value"')
    except JsonSyntaxError as e:
        print(e)

    try:
        parse('{"example2": ] ')
    except JsonSyntaxError as e:
        print(e)

    try:
        parse('{"example3": "value", "example4": }')
    except JsonSyntaxError as e:
        print(e)

    try:
        parse('{"example4": [1, 2, 3, ], "example5": "value"}') 
    except JsonSyntaxError as e:
        print(e)

    try:
        parse('{"example6": "value", "example7": "value"},')
    except JsonSyntaxError as e:
        print(e)

if __name__ == '__main__':  
    test()

# =================== JSON SYNTAX ERROR ===================
# Error Type: JsonUnexpectedToken
# Unexpected Token at line 1, column 14.
# Problematic Character: '"'
# ======================== CONTEXT ========================
# {"example1": "value"
#              ^
# =========================================================
# =================== JSON SYNTAX ERROR ===================
# Error Type: JsonMissingValue
# Missing Value at line 1, column 14.
# Problematic Character: ']'
# ======================== CONTEXT ========================
# {"example2": ] 
#              ^
# =========================================================
# =================== JSON SYNTAX ERROR ===================
# Error Type: JsonMissingValue
# Missing Value at line 1, column 35.
# Problematic Character: '}'
# ======================== CONTEXT ========================
# {"example3": "value", "example4": }
#                                   ^
# =========================================================
# =================== JSON SYNTAX ERROR ===================
# Error Type: JsonMissingValue
# Missing Value at line 1, column 24.
# Problematic Character: ']'
# ======================== CONTEXT ========================
# {"example4": [1, 2, 3, ], "example5": "value"}
#                        ^
# =========================================================
# =================== JSON SYNTAX ERROR ===================
# Error Type: JsonTrailingComma
# Trailing Comma at line 1, column 43.
# Problematic Character: ','
# ======================== CONTEXT ========================
# example6": "value", "example7": "value"},
#                                         ^
# =========================================================