#/file_intro
"""
Module d'analyse d'un fichier source python
contient les classes de données ainsi que la classe Analyse qui se charge du parsing

Raises:
    IndexError: raise IndexError si la classe Analyse détecte une parenthèse non fermée 
    empêchant la détection de la fin d'une fonction
"""


#/actual_version : 1.2.0
#/last_release_date : 20/02/2026                         
#/author : Ywan GERARD


from importlib.resources import files
import json
from pathlib import Path
import re
import sys
from .objects import *
from .generator import MarkdownGenerator



class Parser:
    """
    Cette classe parcours le fichier source, identifie les classes et fonctions
    et identifie les docstrings présents pour chaque classe et fonction
    """

    def __init__(self, path, automatic : bool = True):
        """
        initialise les attributs de la classe :
        -fpath contient le chemin vers le fichier source
        -fname contient le nom du fichier source
        -parse est une liste contenant les classes et fonctions indépendantes scrappées
        -intro contient le docstring en en-tête du fichier source

        Args:
            path (str): chemin vers le fichier source.
            automatic (bool): chemin vers le fichier source.
        """
        self.auto = automatic
        self.fpath = Path(path)
        self.fname = self.fpath.stem
        self.parse : list[Parsed_class, Parsed_function] = []
        self.customs : dict = self.open_custom_config()
        self.file_data : list[Custom_comment] = []
        self.pointer = 0
        self.parse_source()
        if self.auto :
            MarkdownGenerator(self.parse, self.file_data, self.fname)

        

    def get_parse(self): 
         return self.parse


    def parse_source(self):
        """
        parcours le code à la recherche d'une déclaration de classe, de fonction
        et recherche un docstring rattaché à aucune classe ni fonction
        ce docstring indépendant est interprété comme une explication du fichier source
        """
        source : list[str]= self.get_source()
        print("classes and functions found :")
        while  self.pointer < len(source):
            if self.is_class(source[ self.pointer]): 
                print(source[ self.pointer])
                self.pointer += self.class_parser(source[ self.pointer:])

            elif self.is_function(source[ self.pointer:]): 
                print(source[ self.pointer])
                self.pointer += self.function_parser(source[ self.pointer:])

            elif custom:=self.is_custom(source[ self.pointer]) :
                self.pointer += self.parse_custom(custom, source[self.pointer:])

            else :
                self.pointer += 1

    
    def is_custom(self, line : str) -> bool:
        for custom in self.customs:
            if custom in line :
                return custom
        return False
    

    def parse_custom(self, custom : str, lines : list[str]):
        pointer = 0
        content = ""
        match custom :
            case "#/file_intro" :
                pointer += 1
                if self.is_oneline_docstring(lines[pointer]) : 

                    content = self.format_string(lines[pointer].replace('"""', ""))
                    pointer +=1

                elif self.is_docstring(lines[pointer]) : 
                    content = self.format_string(lines[pointer].replace('"""', ""))
                    pointer +=1
                    while not self.is_docstring(lines[pointer]):
                        content += self.format_string(lines[pointer].replace('"""', "")).replace("\t", "")
                        pointer +=1
                    pointer +=1
                    
            case _ :
                content = lines[pointer].replace(custom, "").replace("\n", "")
                pointer += 1
        obj = Custom_comment(self.customs[custom]["type"], self.customs[custom]["ref"], self.customs[custom]["is_list"], content )
        self.file_data.append(obj)
        return pointer


    def is_class(self, line: str) -> bool:
        """
        Vérifie si une ligne est une déclaration de classe

        Args:
            line (str): ligne à vérifier

        Returns:
            bool: retourne True si la ligne est une déclaration de classe, False sinon
        """
        return bool(re.search(r"^class\s.*:", line))
    

    def is_function(self, lines : list[str], in_class = False) -> bool:
        """
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
        """
        if not in_class : pat = r"^def\s+[a-zA-Z_]\w*\s*\(.*"
        else : pat = r"^\s+def\s+[a-zA-Z_]\w*\s*\(.*"
        pointer = 0

        if re.search(pat, lines[0]) :
            opened = lines.count("(") - lines.count(")")
            while opened != 0 and pointer < len(lines):
                pointer += 1
                opened += lines.count("(") - lines.count(")")
            if opened == 0:
                return True
            if not opened and pointer >= len(lines):
                raise IndexError(f"a parenthesis was opened but never closed on line \n {lines[0]}\nFailed to parse the module")
        else :
            return False


    def get_function_declaration(self, lines : list[str]) -> tuple[str, int]:
        """
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
        """
        decla = ""
        pointer = 0

        opened = lines[pointer].count("(") - lines[pointer].count(")")
        decla = lines[0]
        while opened != 0 and pointer < len(lines):
            pointer += 1
            opened += lines[pointer].count("(") - lines[pointer].count(")")
            decla += lines[pointer]
        if opened == 0:
            return self.format_string(decla), pointer + 1
        if not opened and pointer >= len(lines):
            raise IndexError(f"a parenthesis was opened but never closed on line \n {lines[0]}\nFailed to parse the module")


    def class_parser(self, sub_source : list[str]) -> int: 
        """
        isole la déclaration d'une classe, son docstring éventuel,
        puis parcours le code de la classe à la recherche de méthodes

        Args:
            sub_source (list[str]): code source commençant à partir de la déclaration de la classe

        Returns:
            int: retourne la taille de la classe en nombre de ligne, évite que le parseur principal repasse sur du code déjà parsé
        """
        obj = Parsed_class(sub_source[0], "")
        pointer = 1
        docstring = ""
        while pointer < len(sub_source) and not self.is_class(sub_source[pointer]) and not self.is_function(sub_source[pointer:]) :

            if self.is_oneline_docstring(sub_source[pointer]) : 
                docstring = self.format_string(sub_source[pointer].replace('"""', ""))
                pointer +=1

            elif self.is_docstring(sub_source[pointer]) : 
                docstring += self.format_string(sub_source[pointer].replace('"""', ""))
                pointer +=1
                while not self.is_docstring(sub_source[pointer]):
                    docstring += self.format_string(sub_source[pointer].replace('"""', ""))
                    pointer +=1
                pointer +=1

            elif self.is_function(sub_source[pointer:], in_class=True) : 
                print(sub_source[pointer])
                pointer += self.function_parser(sub_source[pointer:], obj)

            else :
                pointer += 1
        obj.docstring = docstring
        self.parse.append(obj)
        return pointer


    def function_parser(self, sub_source : list[str], parent : Parsed_class = None) -> int:
        """
        isole la déclaration d'une fonction et récupère son docstring éventuel,

        Args:
            sub_source (list[str]): code source commençant à partir de la déclaration de la fonction
            parent (Parsed_class, optional): si le paramètre est fourni, alors function_parser
            considèrera que la fonction à scraper est une méthode appartenant à la classe "parent". Defaults to None.

        Returns:
            int: retourne la taille de la fonction en nombre de ligne, évite que le parseur principal repasse sur du code déjà parsé
        """        
        declaration, pointer = self.get_function_declaration(sub_source)
        docstring = ""
        while pointer < len(sub_source) \
            and not self.is_function(sub_source[pointer:], in_class=True) \
            and not self.is_class(sub_source[pointer]) \
            and not self.is_function(sub_source[pointer:]) :
                
                if self.is_oneline_docstring(sub_source[pointer]) : 

                    docstring = self.format_string(sub_source[pointer].replace('"""', ""))
                    pointer +=1

                elif self.is_docstring(sub_source[pointer]) : 
                    docstring += self.format_string(sub_source[pointer].replace('"""', ""))
                    pointer +=1
                    while not self.is_docstring(sub_source[pointer]):
                        docstring += self.format_string(sub_source[pointer].replace('"""', ""))
                        pointer +=1
                    pointer +=1
                else :
                    pointer += 1
        obj = Parsed_function(declaration, docstring)    
        if parent :
            parent.add_method(obj)
        else :
            self.parse.append(obj)
        return pointer
    

    def is_docstring(self, line: str) -> bool:
        """
        Vérifie si une ligne est le début d'un docstring sur plusieurs lignes

        Args:
            line (str): ligne à vérifier

        Returns:
            bool: retourne True si il s'agit du début d'un docstring, False sinon
        """
        return bool(re.search(r"(?<!')\"{3}", line))
    

    def is_oneline_docstring(self, line: str) -> bool:
        """
        Vérifie si une ligne est une doctring sur une seule ligne, par exemple :

        '''doctring d'une fonction'''

        Args:
            line (str): ligne à vérifier

        Returns:
            bool: retourne True si il s'agit d'un docstring sur une ligne, False sinon
        """
        return line.count('"""') == 2


    def format_string(self, string : str) -> str :
        """
        Formate le string passé en paramètre,
        remplace les chaine de tabs supérieures à 3 par une double tab,
        si aucune tab n'est présente dans la chaine, la fonction en ajoute une en début de chaine

        Args:
            string (str): string à traiter

        Returns:
            str: retourne la chaine traité selon l'algorithme défini plus haut
        """
        string = re.sub(r"\s{4}", "\t", string)
        if "\t" in string :
            nb_tab : str = "\t" * string.count("\t")

            string = string.replace(nb_tab, "\t")
        else :
            string = "\t" + string
        return string


    def get_source(self) -> list[str]:
        """
        Ouvre et retourne le code source du fichier choisi

        Returns:
            list[str]: retourne une liste dont chaque élément est une ligne du fichier source à parser
        """
        with open(self.fpath, 'r', encoding='utf-8') as f:
            return f.readlines()


    @staticmethod
    def open_custom_config() -> dict:
        with open(files("easydoc.config").joinpath("custom_comment_lines.json"), 'r', encoding='utf-8') as f :
            return json.load(f)
    

if __name__ == "__main__" :
    if len(sys.argv) >= 2 :
        path = sys.argv[1]
        Parser(path)
    else :
        raise IndexError("Aucun fichier source fourni, arrêt du programme")