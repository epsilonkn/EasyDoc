#/actual_version : 1.1.0
#/TODO Update parsed object for decorators and nested classes
#/file_intro
"""
This module declares the parsed object containers that represent file structure,
function and class metadata, and extracted custom comments.
"""

import re


class Parsed_file:
    """Represents a parsed Python file and its content."""

    def __init__(self, name : str, content_list : list["Parsed_class", "Parsed_function"], file_data : list["Custom_comment"]):
        """Initialize a parsed file container.

        Args:
            name (str): The file name or file path.
            content_list (list[Parsed_class, Parsed_function]): Parsed classes and functions.
            file_data (list[Custom_comment]): Custom comments extracted from the file.
        """
        self.name = name
        self.content_list = content_list
        self.file_data = file_data

class Parsed_function:
    """Represents a parsed function """

    def __init__(self, declaration, docstring):
        """Initialize a parsed function.

        Args:
            declaration (str): The declaration line or block containing the def.
            docstring (str): The docstring content associated with the declaration.
        """
        self.name : str = ""
        self.declaration : str = ""
        self.set_declaration(declaration)
        self.docstring : str = docstring


    def set_declaration(self, declaration):
        """Extract the function name from the declaration.

        Args:
            declaration (str): The function declaration string.
        """
        self.declaration = declaration
        self.name = re.search(r"^\s*def\s+([a-zA-Z_]\w*)", declaration).group(1)

    
    def __str__(self):
        """Return the parsed element name."""
        return self.name


class Custom_comment:
    """Represents a custom comment block extracted from source files."""

    def __init__(self, type_, ref, is_list, content):
        """Initialize a custom comment block.

        Args:
            type_ (str): The type of custom comment.
            ref (str): The reference token used to replace custom comment placeholders.
            is_list (bool): Whether the comment should be treated as a list.
            content (str): The comment content.
        """
        self.type_ : str = type_
        self.ref : str = ref
        self.is_list : bool = is_list
        self.content : str = content


class Parsed_class:
    """Represents a parsed class and its methods."""

    def __init__(self, declaration, docstring):
        """Initialize a parsed class.

        Args:
            declaration (str): The class declaration string.
            docstring (str): The class docstring content.
        """
        self.name : str = ""
        self.declaration : str = ""
        self.set_declaration(declaration)
        self.docstring : str = docstring
        self.methods : list[Parsed_function] = []


    def set_declaration(self, declaration):
        """Extract the class name from the declaration.

        Args:
            declaration (str): The class declaration string.
        """
        self.declaration = declaration
        self.name = re.search(r"^\s*class\s+([a-zA-Z_]\w*)", declaration).group(1)


    def add_method(self, method : Parsed_function):
        """Add a method to the parsed class.

        Args:
            method (Parsed_function): The parsed method to add.
        """
        self.methods.append(method)


    def __str__(self):
        """Return the class name."""
        return self.name

