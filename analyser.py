#-----------------------------------------------------------------------------------------
# Fichier : analyser.py
# Version : 0.1
# Dernier changement : 17/02/2026                         
# dernier éditeur : Ywan GERARD
# Créateur : Ywan GERARD
#
#-----------------------------------------------------------------------------------------

from pathlib import Path
import re


class Parsed_function:

    def __init__(self, declaration, docstring):
        self.declaration : str = declaration
        self.docstring : str = docstring



class Parsed_class:

    def __init__(self, declaration, docstring):
        self.declaration : str = declaration
        self.docstring : str = docstring
        self.methods : list[Parsed_function] = []


    def add_method(self, method : Parsed_function):
        self.methods.append(method)



class Analyse:
    """
    Cette classe parcours le fichier source, identifie les classes et fonctions
    et identifie les docstrings présents pour chaque classe et fonction
    """

    def __init__(self, path : str = ""):
        self.fpath = Path("..\Log-Manager\log.py")
        self.parse : list[Parsed_class, Parsed_function] = []
        self.parse_source()


    def parse_source(self):
        source : list[str]= self.get_source()
        pointer = 0
        while pointer < len(source):
            if self.is_class(source[pointer]): 
                print(source[pointer]) # délencher le parseur de classes
                pointer += self.class_parser(source[pointer:])
            elif self.is_function(source[pointer]): 
                print(source[pointer]) # délencher le parseur de fonction
                pointer += self.function_parser(source[pointer:])
            else :
                pointer += 1


    def is_class(self, line: str):
        return  re.search(r"^class\s.*:", line)
    

    def is_function(self, line : str, in_class = False) -> bool:
        """
        Vérifie si la ligne du pointer est une déclaration de fonction

        Args:
            line (str): ligne à vérifier
            in_class (bool, optional): indique si il s'agit d'une méthode ou d'une fonction. Defaults to False.

        Returns:
            bool: retourne True si il s'agit d'une déclaration de fonction, False sinon
        """

        if not in_class : pat = r"^def\s+[a-zA-Z_]\w*\s*\(.*\).*\s*:"
        else : pat = r"^\s+def\s+[a-zA-Z_]\w*\s*\(.*\).*\s*:"

        return re.search(pat, line)


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

            elif self.is_function(sub_source[pointer], in_class=True) : 
                print(sub_source[pointer])
                pointer += self.function_parser(sub_source[pointer:], obj)

            else :
                pointer += 1
        obj.docstring = docstring
        return pointer


    def function_parser(self, sub_source : list[str], parent : Parsed_class = None) -> int: 
        declaration = sub_source[0]
        pointer =1
        docstring = ""
        while pointer < len(sub_source) and not self.is_function(sub_source[pointer], in_class=True) and not self.is_class(sub_source[pointer]) :
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
    

    def is_docstring(self, line: list[str]) -> str:
        return re.search(r"[^']\"{3}", line)
    
    def is_oneline_docstring(self, line: list[str]) -> str:
        return line.count('"""') == 2


    def get_source(self):
        with open(self.fpath, 'r', encoding='utf-8') as f:
            return f.readlines()
        

if __name__ == "__main__" :
    Analyse()