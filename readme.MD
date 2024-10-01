# LarkJSONParser

An example code of parsing JSON text into an utilizable structure with Lark library.

### Directories
- `json.lark`: A LARK based grammar for parsing JSON(JavaScript Object Notation) syntax file.
- `parser.py`: A simple JSON parsing code that restructs JSON text to Python dictionary completely.
- `parser_for_tree.py`: A modified JSON parser using `Transformer` to build a customized tree. (Can be applied for a such thing like AST(Abstract Syntax Tree))
- `parser_error_handling.py`: A modified JSON parser gracefully handling parss failures due to grammatically incorrect inputs like compilers or interpreters.