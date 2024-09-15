# Parsing JSON data into a tree which is a common apporach in parsing 
# programming language codes by parsers to build abstract syntax tree(AST)s.
from lark import Lark, Transformer
from rich import print
from rich.tree import Tree

# Defining custom objects comprising JSON(Python dictionary) objects
class Number:
    def __init__(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Value must be a number")
        if isinstance(value, int):
            self.type = "int"
            self.value = value
        else:
            self.type = "float"
            self.value = value

    def __repr__(self):
        return f"Number(type={self.type}, value={self.value})"
    
class String:
    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        self.value = value
        self.length = len(value)

    def __repr__(self):
        return f"String(value={self.value}, length={self.length})"
    
class List:
    def __init__(self, items):
        if not isinstance(items, list):
            raise ValueError("Items must be a list")
        self.items = items
        self.length = len(items)

    def __repr__(self):
        return f"List(items={self.items}, length={self.length})"


class Dictionary:
    def __init__(self, items):
        if not isinstance(items, dict):
            raise ValueError("Items must be a dictionary")
        self.items = items

    def __repr__(self):
        return f"Dictionary(items={self.items})"


# Define a custom Lark transformer that converts the Lark-parsed tree into custom tree
class JSONTransformer(Transformer):
    """
    A custom Lark transformer that converts the Lark-parsed tree into custom tree.
    """
    def string(self, string_token):
        return String(string_token[0][1:-1])
    
    def number(self, number_token):
        if '.' in number_token[0]:
            return Number(float(number_token[0]))
        else:
            return Number(int(number_token[0]))

    def list(self, items):
        return List(items)
    
    def pair(self, key_value):
        key, value = key_value
        return key, value
    
    def dict(self, items):
        return Dictionary(dict(items))

# Function to recursively build the tree and dispaly via rich.Tree
def build_rich_tree(node, tree=None):
    if tree is None:
        tree = Tree("JSON Root")

    if isinstance(node, Dictionary):
        dict_tree = tree.add("Dictionary")
        for key, value in node.items.items():
            pair_tree = dict_tree.add(f"Key: {key}")
            build_rich_tree(value, pair_tree)
    elif isinstance(node, List):
        list_tree = tree.add(f"List (length={node.length})")
        for item in node.items:
            build_rich_tree(item, list_tree)
    elif isinstance(node, String):
        tree.add(f"String: '{node.value}' (length={node.length})")
    elif isinstance(node, Number):
        tree.add(f"Number: {node.value} (type={node.type})")
    else:
        tree.add(f"Unknown type: {node}")

    return tree

# Example JSON parsing
with open('json.lark', 'r') as file:
    lark_definition = file.read()

json_parser = Lark(lark_definition, start="value")
json_text = '{"name": "Lyza", "age": 21, "skills": {"languages": ["C", "Python"], "fields": ["system", "cybersecurity", "computer theory"]}}'

tree = json_parser.parse(json_text)
result = JSONTransformer().transform(tree)

# Build the rich tree and print it
rich_tree = build_rich_tree(result)
print(rich_tree)

# JSON Root
# └── Dictionary
#     ├── Key: String(value=name, length=4)
#     │   └── String: 'Lyza' (length=4)
#     ├── Key: String(value=age, length=3)
#     │   └── Number: 21 (type=int)
#     └── Key: String(value=skills, length=6)
#         └── Dictionary
#             ├── Key: String(value=languages, length=9)
#             │   └── List (length=2)
#             │       ├── String: 'C' (length=1)
#             │       └── String: 'Python' (length=6)
#             └── Key: String(value=fields, length=6)
#                 └── List (length=3)
#                     ├── String: 'system' (length=6)
#                     ├── String: 'cybersecurity' (length=13)
#                     └── String: 'computer theory' (length=15)