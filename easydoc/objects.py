import re

class Parsed_function:

    def __init__(self, declaration, docstring):
        self.name : str = ""
        self.declaration : str = ""
        self.set_declaration(declaration)
        self.docstring : str = docstring


    def set_declaration(self, declaration):
        self.declaration = declaration
        self.name = re.search(r"^\s*(?:def|class)\s+([a-zA-Z_]\w*)", declaration).group(1)


class Custom_comment:

    def __init__(self, declaration, docstring):
        self.type_ : str = ""
        self.ref : str = ""
        self.content : str = docstring



class Parsed_class:

    def __init__(self, declaration, docstring):
        self.name : str = ""
        self.declaration : str = ""
        self.set_declaration(declaration)
        self.docstring : str = docstring
        self.methods : list[Parsed_function] = []


    def set_declaration(self, declaration):
        self.declaration = declaration
        self.name = re.search(r"^\s*(?:def|class)\s+([a-zA-Z_]\w*)", declaration).group(1)


    def add_method(self, method : Parsed_function):
        self.methods.append(method)

