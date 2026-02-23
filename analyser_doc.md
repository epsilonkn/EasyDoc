# %nom_module%

# PrÃ©sentation

**Version**
 : 1.1.3

**Author**
 : Ywan GERARD

**Last release date**
 : 20/02/2026                         

**Sum-up**
	
Module d'analyse d'un fichier source python
contient les classes de données ainsi que la classe Analyse qui se charge du parsing

Raises:
IndexError: raise IndexError si la classe Analyse détecte une parenthèse non fermée 
empêchant la détection de la fin d'une fonction


## Utilisation

## DÃ©tail des classes et fonctions
### Classe Parser :
---

Déclaration :

	class Parser:

Description :
	
	Cette classe parcours le fichier source, identifie les classes et fonctions
	et identifie les docstrings présents pour chaque classe et fonction

#### **Methode __init__ :**

Déclaration :

	def __init__(self, path, automatic : bool = True):

Description :

	
	initialise les attributs de la classe :
	-fpath contient le chemin vers le fichier source
	-fname contient le nom du fichier source
	-parse est une liste contenant les classes et fonctions indépendantes scrappées
	-intro contient le docstring en en-tête du fichier source
	
	Args:
	path (str): chemin vers le fichier source.
	automatic (bool): chemin vers le fichier source.

#### **Methode get_parse :**

Déclaration :

	def get_parse(self): 

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
