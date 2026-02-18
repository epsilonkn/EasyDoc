"""
Module d'analyse d'un fichier source python
contient les classes de données ainsi que la classe Analyse qui se charge du parsing

Raises:
    IndexError: raise IndexError si la classe Analyse détecte une parenthèse non fermée 
    empêchant la détection de la fin d'une fonction
"""

#-----------------------------------------------------------------------------------------
# Fichier : analyser.py
# Version : 1
# Dernier changement : 17/02/2026                         
# dernier éditeur : Ywan GERARD
# Créateur : Ywan GERARD
#
#-----------------------------------------------------------------------------------------

from pathlib import Path
import re
import sys
from objects import *
from generator import Generator



class Analyse:
    """
    Cette classe parcours le fichier source, identifie les classes et fonctions
    et identifie les docstrings présents pour chaque classe et fonction
    """

    def __init__(self, path : str = ""):
        self.fpath = Path(path)
        self.fname = self.fpath.stem
        self.parse : list[Parsed_class, Parsed_function] = []
        self.intro = ""
        self.parse_source()


    def parse_source(self):
        source : list[str]= self.get_source()
        pointer = 0
        while pointer < len(source):
            if self.is_oneline_docstring(source[pointer]) : 
                self.intro = source[pointer].replace('"""', "")
                pointer +=1
                print(self.intro)

            elif self.is_docstring(source[pointer]) : 
                self.intro += source[pointer].replace('"""', "")
                pointer +=1
                while not self.is_docstring(source[pointer]):
                    self.intro += source[pointer].replace('"""', "")
                    pointer +=1
                print(self.intro)
                pointer +=1
            elif self.is_class(source[pointer]): 
                print(source[pointer]) # délencher le parseur de classes
                pointer += self.class_parser(source[pointer:])
            elif self.is_function(source[pointer:]): 
                print(source[pointer]) # délencher le parseur de fonction
                pointer += self.function_parser(source[pointer:])
            else :
                pointer += 1
        Generator.run(self.parse, self.intro, self.fname)


    def is_class(self, line: str):
        return  re.search(r"^class\s.*:", line)
    

    def is_function(self, lines : list[str], in_class = False) -> bool:
        """
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
                raise IndexError(f"a parenthesis was openedbut never closed on line \n {lines[0]}\nFailed to parse the module")
        else :
            return False


    def get_function_declaration(self, lines : list[str]) -> str:
        """
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
        """
        decla = ""
        pointer = 0

        opened = lines.count("(") - lines.count(")")
        decla = lines[0]
        while opened != 0 and pointer < len(lines):
            pointer += 1
            opened += lines.count("(") - lines.count(")")
            decla += lines[pointer].replace("\n", "")
        if opened == 0:
            return decla, pointer + 1
        if not opened and pointer >= len(lines):
            raise IndexError(f"a parenthesis was openedbut never closed on line \n {lines[0]}\nFailed to parse the module")


    def class_parser(self, sub_source : list[str]) -> int: 
        obj = Parsed_class(sub_source[0], "")
        pointer = 1
        docstring = ""
        while pointer < len(sub_source) and not self.is_class(sub_source[pointer]) :

            if self.is_oneline_docstring(sub_source[pointer]) : 
                docstring = sub_source[pointer].replace('"""', "")
                pointer +=1
                print(docstring)

            elif self.is_docstring(sub_source[pointer]) : 
                docstring += sub_source[pointer].replace('"""', "")
                pointer +=1
                while not self.is_docstring(sub_source[pointer]):
                    docstring += sub_source[pointer].replace('"""', "")
                    pointer +=1
                print(docstring)
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
        declaration, pointer = self.get_function_declaration(sub_source)
        docstring = ""
        while pointer < len(sub_source) and not self.is_function(sub_source[pointer:], in_class=True) and not self.is_class(sub_source[pointer]) :
            if self.is_oneline_docstring(sub_source[pointer]) : 
                docstring = sub_source[pointer].replace('"""', "")
                pointer +=1
                print(docstring)

            elif self.is_docstring(sub_source[pointer]) : 
                docstring += sub_source[pointer].replace('"""', "")
                pointer +=1
                while not self.is_docstring(sub_source[pointer]):
                    docstring += sub_source[pointer].replace('"""', "")
                    pointer +=1
                print(docstring)
                pointer +=1
            else :
                pointer += 1
        obj = Parsed_function(declaration, docstring)    
        if parent :
            parent.add_method(obj)
        else :
            self.parse.append(obj)
        return pointer
    

    def is_docstring(self, line: str) -> str:
        return re.search(r"(?<!')\"{3}", line)
    
    def is_oneline_docstring(self, line: str) -> str:
        return line.count('"""') == 2


    def get_source(self):
        with open(self.fpath, 'r', encoding='utf-8') as f:
            return f.readlines()
        

if __name__ == "__main__" :
    if sys.argv >= 2 :
        path = sys.argv[1]
        Analyse(path)
    else :
        raise "Aucun fichier source fourni, arrêt du programme"