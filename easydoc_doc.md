# easydoc

## Introduction





## Uses

## Technical details


## Fichier easydoc/classes/exceptions.py :
---

### Classe NotDeveloppedError :
---

Déclaration :

	class NotDeveloppedError(Exception):

Description :
	Raised when a feature is not yet implemented

## Fichier easydoc/classes/parsed_objects.py :
---

### Classe Parsed_file :
---

Déclaration :

	class Parsed_file:

Description :

#### **Methode __init__ :**

Déclaration :

    def __init__(self, name : str, content_list : list["Parsed_class", "Parsed_function"], file_data : list["Custom_comment"]):

### Classe Parsed_function :
---

Déclaration :

	class Parsed_function:

Description :

#### **Methode __init__ :**

Déclaration :

    def __init__(self, declaration, docstring):

#### **Methode set_declaration :**

Déclaration :

    def set_declaration(self, declaration):

#### **Methode __str__ :**

Déclaration :

    def __str__(self):

### Classe Custom_comment :
---

Déclaration :

	class Custom_comment:

Description :

#### **Methode __init__ :**

Déclaration :

    def __init__(self, type_, ref, is_list, content):

### Classe Parsed_class :
---

Déclaration :

	class Parsed_class:

Description :

#### **Methode __init__ :**

Déclaration :

    def __init__(self, declaration, docstring):

#### **Methode set_declaration :**

Déclaration :

    def set_declaration(self, declaration):

#### **Methode add_method :**

Déclaration :

    def add_method(self, method : Parsed_function):

#### **Methode __str__ :**

Déclaration :

    def __str__(self):

## Fichier easydoc/classes/tree_objects.py :
---

### Classe Node :
---

Déclaration :

	class Node:

Description :

#### **Methode __init__ :**

Déclaration :

    def __init__(self, name : str, parent : Union["Node", None] = None, path : str = ""):

#### **Methode add_child :**

Déclaration :

    def add_child(self, child):

#### **Methode full_path :**

Déclaration :

    def full_path(self) -> str:

Description :

	
	return the full path of the leaf by concatenating the name of the leaf and the name of its parent nodes

#### **Methode __str__ :**

Déclaration :

    def __str__(self):

#### **Methode __iter__ :**

Déclaration :

    def __iter__(self):

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
	
	returns 5 for the root node, 3 for child1 and 1 for child2

#### **Methode show_tree :**

Déclaration :

    def show_tree(self, level=0):

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

#### **Methode __init__ :**

Déclaration :

    def __init__(self, name : str, parent : Union["Node", None] = None):

#### **Methode __str__ :**

Déclaration :

    def __str__(self):

#### **Methode __len__ :**

Déclaration :

    def __len__(self):

#### **Methode is_py_leaf :**

Déclaration :

    def is_py_leaf(elt : str) -> bool:

Description :

	
	return true if the string passed represents a Python file, False otherwise

#### **Methode full_path :**

Déclaration :

    def full_path(self) -> str:

Description :

	
	return the full path of the leaf by concatenating the name of the leaf and the name of its parent nodes

## Fichier easydoc/classes/__init__.py :
---

## Fichier easydoc/generators/HTMLGenerator.py :
---

### Classe HTMLGenerator :
---

Déclaration :

	class HTMLGenerator:

Description :

## Fichier easydoc/generators/MarkdownGenerator.py :
---

### Classe MdGenerator :
---

Déclaration :

	class MdGenerator:

Description :

#### **Methode __init__ :**

Déclaration :

    def __init__(self, 
                 debug : bool = False):

#### **Methode _class_wrap :**

Déclaration :

    def _class_wrap(name) : 

#### **Methode _method_wrap :**

Déclaration :

    def _method_wrap(name) : 

#### **Methode _function_wrap :**

Déclaration :

    def _function_wrap(name) : 

#### **Methode _custom_list_wrap :**

Déclaration :

    def _custom_list_wrap(name) : 

#### **Methode _custom_header_wrap :**

Déclaration :

    def _custom_header_wrap(name) : 

#### **Methode _file_wrap :**

Déclaration :

    def _file_wrap(name) : 

#### **Methode open_pattern :**

Déclaration :

    def open_pattern():

#### **Methode open_custom_config :**

Déclaration :

    def open_custom_config() -> dict:

#### **Methode create_file :**

Déclaration :

    def create_file(name, body):

#### **Methode generate_custom_list :**

Déclaration :

    def generate_custom_list(self, customs : list[Custom_comment], type_):

#### **Methode generate_class :**

Déclaration :

    def generate_class(self, classe : Parsed_class):

#### **Methode generate_function :**

Déclaration :

    def generate_function(self, func : Parsed_function, in_class : bool = False):

### Classe OneFileMdGenerator :
---

Déclaration :

	class OneFileMdGenerator(MdGenerator):

Description :

#### **Methode __init__ :**

Déclaration :

    def __init__(self, obj_list : list[Parsed_class, Parsed_function], custom_list : list[Custom_comment], fname : str, debug : bool = False):

### Classe DirMdGenerator :
---

Déclaration :

	class DirMdGenerator(MdGenerator):

Description :

#### **Methode __init__ :**

Déclaration :

    def __init__(self, 
                 file_list : list[Node, Leaf], 
                 dirname : str, 
                 main : str = None,
                 debug : bool = False):

## Fichier easydoc/generators/__init__.py :
---

## Fichier easydoc/main_manager/FileParser.py :
---

### Classe Parser :
---

Déclaration :

	class Parser:

Description :
	
	Cette classe parcours le fichier source, identifie les classes et fonctions
	et identifie les docstrings présents pour chaque classe et fonction

#### **Methode __init__ :**

Déclaration :

    def __init__(self, path, debug=False) -> None:

Description :

	
	initialise les attributs de la classe :
	-fpath contient le chemin vers le fichier source
	-fname contient le nom du fichier source
	-parse est une liste contenant les classes et fonctions indépendantes scrappées
	-intro contient le docstring en en-tête du fichier source
	
	Args:
	path (str): chemin vers le fichier source.

#### **Methode get_parse :**

Déclaration :

    def get_parse(self) -> list[Parsed_class, Parsed_function]:

Description :

	
	retourne la liste des classes et fonctions scrappées
	
	Returns:
	list[Parsed_class, Parsed_function]: retourne la liste des classes et fonctions scrappées

#### **Methode get_file_data :**

Déclaration :

    def get_file_data(self) -> list[Custom_comment]:

Description :

	
	retourne la liste des commentaires personnalisés scrappés
	
	Returns:
	list[Custom_comment]: retourne la liste des commentaires personnalisés scrappés

#### **Methode parse_source :**

Déclaration :

    def parse_source(self):

Description :

	
	parcours le code à la recherche d'une déclaration de classe, de fonction
	et recherche un docstring rattaché à aucune classe ni fonction
	ce docstring indépendant est interprété comme une explication du fichier source

#### **Methode is_custom :**

Déclaration :

    def is_custom(self, line : str) -> bool:

#### **Methode parse_custom :**

Déclaration :

    def parse_custom(self, custom : str, lines : list[str]):

#### **Methode is_class :**

Déclaration :

    def is_class(self, line: str) -> bool:

Description :

	
	Vérifie si une ligne est une déclaration de classe
	
	Args:
	line (str): ligne à vérifier
	
	Returns:
	bool: retourne True si la ligne est une déclaration de classe, False sinon

#### **Methode is_function :**

Déclaration :

    def is_function(self, lines : list[str], in_class = False) -> bool:

Description :

	
	Vérifie si la ligne du pointer est une fonction, ou le début d'une fonction dont l'en-tête est sur plusieurs lignes :
	ex : 
	
	def funct( param1 = "foo", param2 = ("poo", 1)) -> None:
	
	ou
	
	def funct(
	param1 = "foo",
	param2 = ("poo", 1)
	) -> None:
	
	Args:
	line (list[str]): lignes à vérifier
	in_class (bool, optional): indique si il s'agit d'une méthode ou d'une fonction. Defaults to False.
	
	Returns:
	bool: retourne True si il s'agit d'une déclaration de fonction, False sinon

#### **Methode get_function_declaration :**

Déclaration :

    def get_function_declaration(self, lines : list[str]) -> tuple[str, int]:

Description :

	
	Récupère la déclaration de la fonction et la retoure
	ex : 
	
	def funct( param1 = "foo", param2 = ("poo", 1)) -> None:
	
	ou
	
	def funct(
	param1 = "foo",
	param2 = ("poo", 1)
	) -> None:
	
	Args:
	line (list[str]): lignes où se trouvent la déclaration
	in_class (bool, optional): indique si il s'agit d'une méthode ou d'une fonction. Defaults to False.
	
	Returns:
	str: retourne la déclaration de la fonction sous forme d'un string

#### **Methode class_parser :**

Déclaration :

    def class_parser(self, sub_source : list[str]) -> int: 

Description :

	
	isole la déclaration d'une classe, son docstring éventuel,
	puis parcours le code de la classe à la recherche de méthodes
	
	Args:
	sub_source (list[str]): code source commençant à partir de la déclaration de la classe
	
	Returns:
	int: retourne la taille de la classe en nombre de ligne, évite que le parseur principal repasse sur du code déjà parsé

#### **Methode function_parser :**

Déclaration :

    def function_parser(self, sub_source : list[str], parent : Parsed_class = None) -> int:

Description :

	
	isole la déclaration d'une fonction et récupère son docstring éventuel,
	
	Args:
	sub_source (list[str]): code source commençant à partir de la déclaration de la fonction
	parent (Parsed_class, optional): si le paramètre est fourni, alors function_parser
	considèrera que la fonction à scraper est une méthode appartenant à la classe "parent". Defaults to None.
	
	Returns:
	int: retourne la taille de la fonction en nombre de ligne, évite que le parseur principal repasse sur du code déjà parsé

#### **Methode is_docstring :**

Déclaration :

    def is_docstring(self, line: str) -> bool:

Description :

	
	Vérifie si une ligne est le début d'un docstring sur plusieurs lignes
	
	Args:
	line (str): ligne à vérifier
	
	Returns:
	bool: retourne True si il s'agit du début d'un docstring, False sinon

#### **Methode is_oneline_docstring :**

Déclaration :

    def is_oneline_docstring(self, line: str) -> bool:

Description :

	
	Vérifie si une ligne est une doctring sur une seule ligne, par exemple :
	
	'''doctring d'une fonction'''
	
	Args:
	line (str): ligne à vérifier
	
	Returns:
	bool: retourne True si il s'agit d'un docstring sur une ligne, False sinon

#### **Methode format_string :**

Déclaration :

    def format_string(self, string : str) -> str :

Description :

	
	Formate le string passé en paramètre,
	remplace les chaine de tabs supérieures à 3 par une double tab,
	si aucune tab n'est présente dans la chaine, la fonction en ajoute une en début de chaine
	
	Args:
	string (str): string à traiter
	
	Returns:
	str: retourne la chaine traité selon l'algorithme défini plus haut

#### **Methode get_source :**

Déclaration :

    def get_source(self) -> list[str]:

Description :

	
	Ouvre et retourne le code source du fichier choisi
	
	Returns:
	list[str]: retourne une liste dont chaque élément est une ligne du fichier source à parser

#### **Methode open_custom_config :**

Déclaration :

    def open_custom_config() -> dict:

## Fichier easydoc/main_manager/InteractiveManager.py :
---

### Classe InteractiveManager :
---

Déclaration :

	class InteractiveManager:

Description :

#### **Methode is_valid_path :**

Déclaration :

    def is_valid_path(path: str) -> bool:

Description :

	Check if the given path is valid and points to a python file or a directory

#### **Methode run :**

Déclaration :

    def run(cls, default_args : dict) -> dict:

## Fichier easydoc/main_manager/TreatmentManager.py :
---

### Classe TreatmentManager :
---

Déclaration :

	class TreatmentManager:

Description :

#### **Methode __init__ :**

Déclaration :

    def __init__(self, path: str, type: str, format: str, recursive: bool = False, onefile: bool = False, main: str = None, debug: bool = False) -> None:

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

#### **Methode get_default_args :**

Déclaration :

    def get_default_args():

#### **Methode _parse_file :**

Déclaration :

    def _parse_file(self, path: str) -> tuple[list[Parsed_class, Parsed_function], list[Custom_comment]]:

Description :

	Treat a single file and generate its documentation

#### **Methode _search_file :**

Déclaration :

    def _search_file(self, path: str, parent : Node | None = None) -> Node:

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

## Fichier easydoc/main_manager/__init__.py :
---

## Fichier easydoc/__init__.py :
---

## Fichier easydoc/__main__.py :
---

### Fonction is_valid_path :

Déclaration :

def is_valid_path(path: str) -> bool:

Description :

	Check if the given path is valid and points to a python file or a directory
