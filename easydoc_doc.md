# easydoc

## Introduction

**Version**
 : 1.0.0

**Sum-up**
	
This package initializer exposes the parsed object and tree classes
needed by the EasyDoc core modules.


## Uses

## Technical details


## Fichier easydoc/classes/exceptions.py :
---

### Classe NotDeveloppedError :
---

Déclaration :

	class NotDeveloppedError(Exception):

Description :
	Raised when a feature is not yet implemented.

## Fichier easydoc/classes/parsed_objects.py :
---

### Classe Parsed_file :
---

Déclaration :

	class Parsed_file:

Description :
	Represents a parsed Python file and its content.

#### **Methode __init__ :**

Déclaration :

    def __init__(self, name : str, content_list : list["Parsed_class", "Parsed_function"], file_data : list["Custom_comment"]):

Description :

	Initialize a parsed file container.
	
	Args:
	name (str): The file name or file path.
	content_list (list[Parsed_class, Parsed_function]): Parsed classes and functions.
	file_data (list[Custom_comment]): Custom comments extracted from the file.

### Classe Parsed_function :
---

Déclaration :

	class Parsed_function:

Description :
	Represents a parsed function 

#### **Methode __init__ :**

Déclaration :

    def __init__(self, declaration, docstring):

Description :

	Initialize a parsed function.
	
	Args:
	declaration (str): The declaration line or block containing the def.
	docstring (str): The docstring content associated with the declaration.

#### **Methode set_declaration :**

Déclaration :

    def set_declaration(self, declaration):

Description :

	Extract the function name from the declaration.
	
	Args:
	declaration (str): The function declaration string.

#### **Methode __str__ :**

Déclaration :

    def __str__(self):

Description :

	Return the parsed element name.

### Classe Custom_comment :
---

Déclaration :

	class Custom_comment:

Description :
	Represents a custom comment block extracted from source files.

#### **Methode __init__ :**

Déclaration :

    def __init__(self, type_, ref, is_list, content):

Description :

	Initialize a custom comment block.
	
	Args:
	type_ (str): The type of custom comment.
	ref (str): The reference token used to replace custom comment placeholders.
	is_list (bool): Whether the comment should be treated as a list.
	content (str): The comment content.

### Classe Parsed_class :
---

Déclaration :

	class Parsed_class:

Description :
	Represents a parsed class and its methods.

#### **Methode __init__ :**

Déclaration :

    def __init__(self, declaration, docstring):

Description :

	Initialize a parsed class.
	
	Args:
	declaration (str): The class declaration string.
	docstring (str): The class docstring content.

#### **Methode set_declaration :**

Déclaration :

    def set_declaration(self, declaration):

Description :

	Extract the class name from the declaration.
	
	Args:
	declaration (str): The class declaration string.

#### **Methode add_method :**

Déclaration :

    def add_method(self, method : Parsed_function):

Description :

	Add a method to the parsed class.
	
	Args:
	method (Parsed_function): The parsed method to add.

#### **Methode __str__ :**

Déclaration :

    def __str__(self):

Description :

	Return the class name.

## Fichier easydoc/classes/tree_objects.py :
---

### Classe Node :
---

Déclaration :

	class Node:

Description :
	Represents a tree node that can contain child nodes and leaves.

#### **Methode __init__ :**

Déclaration :

    def __init__(self, name : str, parent : Union["Node", None] = None, path : str = ""):

Description :

	Initialize a tree node.
	
	Args:
	name (str): The name of the node.
	parent (Union["Node", None]): The parent node, or None for a root node.
	path (str): Optional path string used by the node.

#### **Methode full_path :**

Déclaration :

    def full_path(self) -> str:

Description :

	Return the full path of this node by concatenating parent names.

#### **Methode show_tree :**

Déclaration :

    def show_tree(self, level=0):

Description :

	Print the tree structure rooted at this node.
	
	Args:
	level (int): Current indentation level for recursive display.

#### **Methode add_child :**

Déclaration :

    def add_child(self, child : Union["Node", "Leaf"]):

Description :

	Add a child node or leaf to this node.
	
	Args:
	child (Union["Node", "Leaf"]): Child element to attach.

#### **Methode __str__ :**

Déclaration :

    def __str__(self):

Description :

	Return the node name.

#### **Methode __iter__ :**

Déclaration :

    def __iter__(self):

Description :

	Iterate over the node and its subtree in depth-first order.
	
	Yields:
	Union["Node", "Leaf"]: Each node or leaf in the tree.

#### **Methode __len__ :**

Déclaration :

    def __len__(self) -> int:

Description :

	
	returns the sum of all the elements in the tree
	
	ex :
	root
	├── child1
	│   ├── child1.1
	│   └── child1.2
	└── child2
	
	returns 5 for the root node, 3 for child1, 1 for child2 and 1 for the root

#### **Methode __truediv__ :**

Déclaration :

    def __truediv__(self, elt : Union["Node", "Leaf", str]) -> Union["Node", "Leaf"]:

Description :

	
	Allows to create a path by using the division operator, for example :
	
	root = Node("root")
	
	root / "child1" / "child1.1"
	
	will create the following tree :
	
	root
	└── child1
	└── child1.1
	
	Args:
	elt (Union["Node", "Leaf", str]): the element to add to the tree, it can be either a string, a Node or a Leaf
	
	Raises:
	TypeError: Raised when the type of the element is not valid, the element must be either a string, a Node or a Leaf.
	
	Returns:
	Union["Node", "Leaf"]: returns the created node or leaf

### Classe Leaf :
---

Déclaration :

	class Leaf:

Description :
	Represents a leaf item in the tree, typically a Python file.

#### **Methode __init__ :**

Déclaration :

    def __init__(self, name : str, parent : Union["Node", None] = None):

Description :

	Initialize a tree leaf.
	
	Args:
	name (str): The name of the leaf.
	parent (Union["Node", None]): The parent node, or None for a detached leaf.

#### **Methode __str__ :**

Déclaration :

    def __str__(self):

Description :

	Return the leaf name.

#### **Methode __len__ :**

Déclaration :

    def __len__(self):

Description :

	Return 1 for a leaf.

#### **Methode is_py_leaf :**

Déclaration :

    def is_py_leaf(elt : str) -> bool:

Description :

	Return True when the string represents a Python file name.
	
	Args:
	elt (str): The string to test.
	
	Returns:
	bool: True when elt ends with .py, False otherwise.

#### **Methode full_path :**

Déclaration :

    def full_path(self) -> str:

Description :

	Return the full path of this leaf by concatenating parent names.

## Fichier easydoc/classes/__init__.py :
---

## Fichier easydoc/core/FileParser.py :
---

### Classe Parser :
---

Déclaration :

	class Parser:

Description :
	Parse Python source files and extract structured metadata.

#### **Methode __init__ :**

Déclaration :

    def __init__(self, path, debug=False) -> None:

Description :

	Initialize the parser and immediately start parsing the file.
	
	Args:
	path (str): Path to the source file.
	debug (bool): Enable debug logging.

#### **Methode get_parse :**

Déclaration :

    def get_parse(self) -> list[Parsed_class, Parsed_function]:

Description :

	Return parsed classes and functions from the file.
	
	Returns:
	list[Parsed_class, Parsed_function]: The parsed classes and functions.

#### **Methode get_file_data :**

Déclaration :

    def get_file_data(self) -> list[Custom_comment]:

Description :

	Return the custom comment blocks extracted from the file.
	
	Returns:
	list[Custom_comment]: The parsed custom comments.

#### **Methode parse_source :**

Déclaration :

    def parse_source(self):

Description :

	Parse the source file and extract classes, functions, and standalone docstrings.
	
	The standalone docstring in the file is treated as a file-level description.

#### **Methode is_custom :**

Déclaration :

    def is_custom(self, line : str) -> bool:

Description :

	Detect whether the given line contains a custom comment marker.
	
	Args:
	line (str): The source line to inspect.
	
	Returns:
	bool: The custom marker string if found, otherwise False.

#### **Methode parse_custom :**

Déclaration :

    def parse_custom(self, custom : str, lines : list[str]):

Description :

	Parse a custom comment block from the source lines.
	
	Args:
	custom (str): The custom marker to parse.
	lines (list[str]): The source lines starting at the marker location.
	
	Returns:
	int: Number of source lines consumed by the custom block.

#### **Methode is_class :**

Déclaration :

    def is_class(self, line: str) -> bool:

Description :

	Check whether a line declares a class.
	
	Args:
	line (str): The line to inspect.
	
	Returns:
	bool: True if the line declares a class, False otherwise.

#### **Methode is_function :**

Déclaration :

    def is_function(self, lines : list[str], in_class = False) -> bool:

Description :

	Check whether the current lines start a function declaration.
	
	This handles both single-line function headers and multi-line headers.
	
	Args:
	lines (list[str]): The source lines to inspect.
	in_class (bool, optional): Whether the function is indented as a method. Defaults to False.
	
	Returns:
	bool: True if the lines begin a function declaration, False otherwise.

#### **Methode get_function_declaration :**

Déclaration :

    def get_function_declaration(self, lines : list[str]) -> tuple[str, int]:

Description :

	Extract a function declaration block from source lines.
	
	This method returns the full function header and the number of lines consumed.
	
	Args:
	lines (list[str]): The lines beginning at the function declaration.
	
	Returns:
	tuple[str, int]: The function declaration string and the number of lines consumed.

#### **Methode class_parser :**

Déclaration :

    def class_parser(self, sub_source : list[str]) -> int: 

Description :

	Parse a class block and extract its docstring and method definitions.
	
	Args:
	sub_source (list[str]): Source code starting at the class declaration.
	
	Returns:
	int: Number of lines consumed while parsing the class block.

#### **Methode function_parser :**

Déclaration :

    def function_parser(self, sub_source : list[str], parent : Parsed_class = None) -> int:

Description :

	Parse a function or method block and extract its docstring.
	
	Args:
	sub_source (list[str]): Source code starting at the function declaration.
	parent (Parsed_class, optional): If provided, the function is treated as a method of this class.
	Defaults to None.
	
	Returns:
	int: Number of lines consumed while parsing the function block.

#### **Methode is_docstring :**

Déclaration :

    def is_docstring(self, line: str) -> bool:

Description :

	Check whether a line begins a multi-line docstring.
	
	Args:
	line (str): The source line to inspect.
	
	Returns:
	bool: True if the line starts a multi-line docstring, False otherwise.

#### **Methode is_oneline_docstring :**

Déclaration :

    def is_oneline_docstring(self, line: str) -> bool:

Description :

	Check whether a line contains a one-line docstring.
	
	Args:
	line (str): The source line to inspect.
	
	Returns:
	bool: True if the line contains a one-line docstring, False otherwise.

#### **Methode format_string :**

Déclaration :

    def format_string(self, string : str) -> str :

Description :

	Format the given string for proper indentation handling.
	
	This replaces sequences of four spaces with a tab and normalizes tabs.
	If the resulting string has no indentation, a leading tab is added.
	
	Args:
	string (str): The string to format.
	
	Returns:
	str: The formatted string.

#### **Methode get_source :**

Déclaration :

    def get_source(self) -> list[str]:

Description :

	Read and return the source lines of the current file.
	
	Returns:
	list[str]: Source lines of the file.

#### **Methode open_custom_config :**

Déclaration :

    def open_custom_config() -> dict:

Description :

	Load the custom comment marker configuration from package resources.
	
	Returns:
	dict: Loaded configuration for supported custom comment markers.

## Fichier easydoc/core/InteractiveManager.py :
---

### Classe InteractiveManager :
---

Déclaration :

	class InteractiveManager:

Description :
	Manage the interactive mode.
	
	Parse user input to set the arguments for the TreatmentManager and start generation.

#### **Methode _ask_type :**

Déclaration :

    def _ask_type(cls) -> str:

Description :

	
	Ask the user for the document type to treat
	
	Returns:
	str: returns the document type to treat, either "file" or "dir"

#### **Methode _ask_path :**

Déclaration :

    def _ask_path(cls) -> str:

Description :

	
	Ask the user for the path to the file or directory to document
	
	Returns:
	str: returns the path to the file or directory to document

#### **Methode run :**

Déclaration :

    def run(cls) -> dict:

Description :

	Start the interactive prompt and return the selected arguments.
	
	Returns:
	dict: The parsed arguments to pass to TreatmentManager.

## Fichier easydoc/core/TreatmentManager.py :
---

### Classe TreatmentManager :
---

Déclaration :

	class TreatmentManager:

Description :
	Manage the documentation treatment workflow.

#### **Methode __init__ :**

Déclaration :

    def __init__(self, **kwargs) -> None:

Description :

	
	Initialize the treatment and generation of a documentation
	
	Args:
	path (str): path to the file or directory to document
	type (str): type of document to treat, either "file" or "dir"
	format (str): format of the documentation to generate
	recursive (bool): whether to search for Python files recursively in the directory
	onefile (bool): whether to generate a single documentation file for the whole directory
	main (str): path to the main file for the directory
	debug (bool): whether to enable debug mode

#### **Methode _parse_file :**

Déclaration :

    def _parse_file(self, path: str) -> tuple[list[Parsed_class, Parsed_function], list[Custom_comment]]:

Description :

	Treat a single file and generate its documentation

#### **Methode _search_file :**

Déclaration :

    def _search_file(self, path: str, parent : Node | None = None, depth: int = 0) -> Node:

Description :

	Recursively search a directory and build a file tree of Python files.
	
	Args:
	path (str): Directory path to scan.
	parent (Node | None): Optional parent node for tree construction.
	depth (int): Current recursion depth.
	
	Returns:
	Node: The root node of the discovered tree.

#### **Methode _treat_file :**

Déclaration :

    def _treat_file(self, path: str = None):

Description :

	Treat a single file and generate its documentation

#### **Methode _treat_dir :**

Déclaration :

    def _treat_dir(self):

Description :

	Treat a whole directory and generate the documentation for all the files in it

## Fichier easydoc/core/utils/const.py :
---

## Fichier easydoc/core/utils/function_utils.py :
---

### Fonction is_valid_path :

Déclaration :

def is_valid_path(path: str) -> bool:

Description :

	Check if the given path is valid and points to a python file or a directory.

## Fichier easydoc/core/utils/__init__.py :
---

## Fichier easydoc/core/__init__.py :
---

## Fichier easydoc/generators/HTMLGenerator.py :
---

### Classe HTMLGenerator :
---

Déclaration :

	class HTMLGenerator:

Description :
	Represents the HTML generator for EasyDoc.
	
	Currently a placeholder for future HTML documentation generation support.

## Fichier easydoc/generators/MarkdownGenerator.py :
---

### Classe MdGenerator :
---

Déclaration :

	class MdGenerator:

Description :
	Base class for Markdown generators.

#### **Methode __init__ :**

Déclaration :

    def __init__(self, 
                 debug : bool = False):

Description :

	Initialize the markdown generator and load the template resources.
	
	Args:
	debug (bool): Enable debug output during generation.

#### **Methode _class_wrap :**

Déclaration :

    def _class_wrap(name) : 

Description :

	Return a markdown header for a class section.

#### **Methode _method_wrap :**

Déclaration :

    def _method_wrap(name) : 

Description :

	Return a markdown header for a method section.

#### **Methode _function_wrap :**

Déclaration :

    def _function_wrap(name) : 

Description :

	Return a markdown header for a function section.

#### **Methode _custom_list_wrap :**

Déclaration :

    def _custom_list_wrap(name) : 

Description :

	Return a markdown header for a custom list section.

#### **Methode _custom_header_wrap :**

Déclaration :

    def _custom_header_wrap(name) : 

Description :

	Return a markdown header for a custom comment block.

#### **Methode _file_wrap :**

Déclaration :

    def _file_wrap(name) : 

Description :

	Return a markdown header for a file section.

#### **Methode open_pattern :**

Déclaration :

    def open_pattern():

Description :

	Load the Markdown template pattern for documentation output.

#### **Methode open_custom_config :**

Déclaration :

    def open_custom_config() -> dict:

Description :

	Load custom comment configuration from the package resources.

#### **Methode create_file :**

Déclaration :

    def create_file(name, body):

Description :

	Create a documentation file from the generated body.
	
	Args:
	name (str): Base name of the created documentation file.
	body (str): The content to write.

#### **Methode generate_custom_list :**

Déclaration :

    def generate_custom_list(self, customs : list[Custom_comment], type_):

Description :

	Generate documentation for a list of custom comments.
	
	Args:
	customs (list[Custom_comment]): Custom comments to render.
	type_ (str): The type of custom comment list to generate.
	
	Returns:
	str: The generated markdown block for the custom list.

#### **Methode generate_class :**

Déclaration :

    def generate_class(self, classe : Parsed_class):

Description :

	Generate the markdown block for a parsed class.

#### **Methode generate_function :**

Déclaration :

    def generate_function(self, func : Parsed_function, in_class : bool = False):

Description :

	Generate the markdown block for a parsed function or method.

### Classe OneFileMdGenerator :
---

Déclaration :

	class OneFileMdGenerator(MdGenerator):

Description :
	Generate a single markdown documentation file for a list of parsed objects.

#### **Methode __init__ :**

Déclaration :

    def __init__(self, obj_list : list[Parsed_class, Parsed_function], custom_list : list[Custom_comment], fname : str, debug : bool = False):

Description :

	Initialize and generate a documentation markdown file for a single source module.
	
	Args:
	obj_list (list[Parsed_class, Parsed_function]): Parsed classes and functions.
	custom_list (list[Custom_comment]): Custom comments from the source file.
	fname (str): Base name of the output file.
	debug (bool): Enable debug logging.

### Classe DirMdGenerator :
---

Déclaration :

	class DirMdGenerator(MdGenerator):

Description :
	Generate documentation for a directory of Python files.

#### **Methode __init__ :**

Déclaration :

    def __init__(self, 
                 file_list : list[Node, Leaf], 
                 dirname : str, 
                 main : str = None,
                 debug : bool = False):

Description :

	Initialize the directory documentation generator.
	
	Args:
	file_list (list[Node, Leaf]): The file tree nodes and leaves to document.
	dirname (str): The base directory name used for the output file.
	main (str, optional): Optional main file name to use for header selection.
	debug (bool): Enable debug logging.

## Fichier easydoc/generators/__init__.py :
---

## Fichier easydoc/__init__.py :
---

## Fichier easydoc/__main__.py :
---
