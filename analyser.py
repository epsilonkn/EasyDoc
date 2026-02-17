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

    def __init__(self, name, docstring):
        self.name : str = name
        self.docstring : str = docstring



class Parsed_class:

    def __init__(self, name, docstring):
        self.name : str = name
        self.docstring : str = docstring
        self.methods : list[Parsed_function] = []



class Analyse:

    def __init__(self, path : str = ""):
        self.fpath = Path("./analyser.py")
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
        return  re.search(r"class\s.*:", line)
    

    def is_function(self, line : str, in_class = False):
        pat = r"def\s+[a-zA-Z_]\w*\s*\(.*\)\s*:" if not in_class else r"\s+def\s+[a-zA-Z_]\w*\s*\(.*\)\s*:"
        return re.search(pat, line)


    def class_parser(self, sub_source : list[str]) -> int: 
        pointer = 1
        while pointer < len(sub_source) and not self.is_class(sub_source[pointer]) :
            if self.is_function(sub_source[pointer], in_class=True) : 
                print(sub_source[pointer])
                pointer += self.function_parser(sub_source[pointer])
            else :
                pointer += 1
        return pointer


    def function_parser(self, sub_source : list[str]) -> int: 
        pointer =1
        while pointer < len(sub_source) and not self.is_function(sub_source[pointer], in_class=True) and not self.is_class(sub_source[pointer]) :
            if False :
                pass
            else :
                pointer += 1
        return pointer


    def get_source(self):
        with open(self.fpath, 'r', encoding='utf-8') as f:
            return f.readlines()
        

if __name__ == "__main__" :
    Analyse()