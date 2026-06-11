#/actual_version : 1.2.0
#/TODO Update parsed object for decorators and nested classes
#/TODO Take in count the return type of the functions
#/file_intro
"""
This module declares the parsed object containers that represent file structure,
function and class metadata, and extracted custom comments.
"""

import re
from typing import Union


class Parsed_object:

    def __init__(self, name : str, level : int = 0):
        """Initialize a parsed object.

        Args:
            name (str): The file name or file path.
            content_list (list[Parsed_class, Parsed_function]): Parsed classes and functions.
            file_data (list[Custom_comment]): Custom comments extracted from the file.
        """
        self.name = name
        self.content : list["Parsed_object"] = []
        self.comments : list["Custom_comment"] = []
        self.level = level
        self.docstring : str = ""


    def add_content(self, content : Union["Parsed_object"]):
        self.content.append(content)


    def add_comment(self, data : "Custom_comment"):
        self.comments.append(data)



class Parsed_file(Parsed_object):
    """Represents a parsed Python file and its content."""

    def __init__(self, name : str):
        """Initialize a parsed file container.

        Args:
            name (str): The file name or file path.
            content_list (list[Parsed_class, Parsed_function]): Parsed classes and functions.
            file_data (list[Custom_comment]): Custom comments extracted from the file.
        """
        super().__init__(name, 0)
        self.name = name


class Parsed_function(Parsed_object):
    """Represents a parsed function """

    def __init__(self, declaration : str, type_ : str, level : int = 1):
        """Initialize a parsed function.

        Args:
            declaration (str): The declaration line or block containing the def.
            docstring (str): The docstring content associated with the declaration.
        """
        super().__init__("", level)
        self.declaration : str = ""
        self.set_declaration(declaration)
        self.funct_type = type_


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

    def __init__(self, type_ : str, ref : str , title : str, is_list : bool, content : str):
        """Initialize a custom comment block.

        Args:
            type_ (str): The type of custom comment.
            ref (str): The reference token used to replace custom comment placeholders.
            title (str): The title of the custom comment.
            is_list (bool): Whether the comment should be treated as a list.
            content (str): The comment content.
        """
        self.type_ : str = type_
        self.title : str = title
        self.ref : str = ref
        self.is_list : bool = is_list
        self.content : str = content



class Parsed_class(Parsed_object):
    """Represents a parsed class and its methods."""

    def __init__(self, declaration, level : int = 1):
        """Initialize a parsed class.

        Args:
            declaration (str): The class declaration string.
            docstring (str): The class docstring content.
        """
        super().__init__("", level)
        self.declaration : str = ""
        self.set_declaration(declaration)
        self.level = level


    def set_declaration(self, declaration):
        """Extract the class name from the declaration.

        Args:
            declaration (str): The class declaration string.
        """
        self.declaration = declaration
        self.name = re.search(r"^\s*class\s+([a-zA-Z_]\w*)", declaration).group(1)


    def __str__(self):
        """Return the class name."""
        return self.name