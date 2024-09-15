from lark import Lark, Transformer
from rich import print_json

# A Lark transformer that converts the parse tree into a JSON object
class JSONTransformer(Transformer):
    def string(self, string_token):
        # Extract the value from the token, removing quotes
        return string_token[0][1:-1]
    
    def number(self, number_token):
        if '.' in number_token[0]:
            return float(number_token[0])
        else:
            return int(number_token[0])

    def list(self, items):
        return list(items)
    
    def pair(self, key_value):
        key, value = key_value
        return key, value
    
    def dict(self, items):
        return dict(items)

# Load Lark grammar from file
with open('json.lark', 'r') as file:
    lark_definition = file.read()

json_parser = Lark(lark_definition, start="value")
json_text = '{"name": "Lyza", "age": 21, "skills": {"languages": ["C", "Python"], "fields": ["system", "cybersecurity", "computer theory"]}}'

tree = json_parser.parse(json_text)
result = JSONTransformer().transform(tree)

# Print the result which is a parsed JSON object(dictionary)
print_json(data=result)

# Output:
# {
#   "name": "Lyza",
#   "age": 21,
#   "skills": {
#     "languages": [
#       "C",
#       "Python"
#     ],
#     "fields": [
#       "system",
#       "cybersecurity",
#       "computer theory"
#     ]
#   }
# }