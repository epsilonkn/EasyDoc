# analyser

## Présentation


Module d'analyse d'un fichier source python
contient les classes de données ainsi que la classe Analyse qui se charge du parsing

Raises:
    IndexError: raise IndexError si la classe Analyse détecte une parenthèse non fermée 
    empêchant la détection de la fin d'une fonction


## Utilisation

## Détail du contenu



### Classe Analyse :

Déclaration :

	class Analyse:

Description :
    
    Cette classe parcours le fichier source, identifie les classes et fonctions
    et identifie les docstrings présents pour chaque classe et fonction

#### **Methode __init__ :**

Déclaration :

	    def __init__(self, path):

Description :
        
        initialise les attributs de la classe :
        -fpath contient le chemin vers le fichier source
        -fname contient le nom du fichier source
        -parse est une liste contenant les classes et fonctions indépendantes scrappées
        -intro contient le docstring en en-tête du fichier source

        Args:
            path (str): chemin vers le fichier source.

#### **Methode parse_source :**

Déclaration :

	    def parse_source(self):

Description :

#### **Methode is_class :**

Déclaration :

	    def is_class(self, line: str):

Description :

#### **Methode is_function :**

Déclaration :

	    def is_function(self, lines : list[str], in_class = False) -> bool:

Description :
        
        Vérifie si la ligne du pointer est le début d'une fonction dont l'en-tête est sur plusieurs lignes :
        ex : 

        def funct(
            param1 = "foo"
            param2 = ("poo", 1)
        ) -> None:

        Args:
            line (str): ligne à vérifier
            in_class (bool, optional): indique si il s'agit d'une méthode ou d'une fonction. Defaults to False.

        Returns:
            bool: retourne True si il s'agit d'une déclaration de fonction, False sinon

#### **Methode get_function_declaration :**

Déclaration :

	    def get_function_declaration(self, lines : list[str]) -> str:

Description :
        
        Récupère la déclaration de la fonction et la retoure
        ex : 

        def funct(
            param1 = "foo"
            param2 = ("poo", 1)
        ) -> None:

        Args:
            line (str): lignes où se trouve la déclaration
            in_class (bool, optional): indique si il s'agit d'une méthode ou d'une fonction. Defaults to False.

        Returns:
            str: retourne la déclaration de la fonction sous forme d'un string

#### **Methode class_parser :**

Déclaration :

	    def class_parser(self, sub_source : list[str]) -> int: 

Description :

#### **Methode function_parser :**

Déclaration :

	    def function_parser(self, sub_source : list[str], parent : Parsed_class = None) -> int: 

Description :

#### **Methode is_docstring :**

Déclaration :

	    def is_docstring(self, line: str) -> str:

Description :

#### **Methode is_oneline_docstring :**

Déclaration :

	    def is_oneline_docstring(self, line: str) -> str:

Description :

#### **Methode get_source :**

Déclaration :

	    def get_source(self):

Description :
