#-----------------------------------------------------------------------------------------
# Fichier : analyser.py
# Version : 1.1
# Dernier changement : 21/02/2026                         
# dernier éditeur : Ywan GERARD
# Créateur : Ywan GERARD
#
#-----------------------------------------------------------------------------------------

from pathlib import Path

from .objects import Parsed_class, Parsed_function
import os


class MarkdownGenerator:

    markdown : str = "# %nom_module%\n\n# Présentation\n\n%intro%\n\n## Utilisation\n\n## Détail des classes et fonctions\n\n"

    def __init__(self, obj_list, intro, fname):
        body : str= self.markdown
        body = body.replace("%intro%", intro)
        body = body.replace("%nom_module%", fname)
        for elt in obj_list :
            if isinstance(elt, Parsed_class):
                body += self.generate_class(elt)

        for elt in obj_list :
            if isinstance(elt, Parsed_function):
                body += self.generate_function(elt)

        self.create_file(fname, body)

    @staticmethod
    def class_wrap(name) : 
        return f"\n### Classe {name} :\n---\n"
    @staticmethod
    def method_wrap(name) : 
        return f"\n#### **Methode {name} :**\n"
    @staticmethod
    def function_wrap(name) : 
        return f"\n### Fonction {name} :\n"


    @staticmethod
    def open_pattern():
        with open(str(Path(__file__).parent) +"/pattern.md", 'r', encoding="utf-8") as f:
            return f.read()
        
    
    @staticmethod
    def create_file(name, body):
        with open(f"{os.getcwd()}/{name}_doc.md", 'w', encoding="utf-8") as f:
            return f.write(body)


    def generate_class(self, classe : Parsed_class):
        subbody = self.class_wrap(classe.name)
        subbody += f"\nDéclaration :\n\n\t{classe.declaration}"
        subbody += f"\nDescription :\n{classe.docstring}"
        for func in classe.methods:
            subbody += self.generate_function(func, True)

        return subbody


    def generate_function(self, func : Parsed_function, in_class : bool = False):
        if in_class :
            subbody = self.method_wrap(func.name)
        else : 
            subbody = self.function_wrap(func.name)

        
        subbody += f"\nDéclaration :\n\n{func.declaration}"
        if func.docstring:
            subbody += f"\nDescription :\n\n{func.docstring}"

        return subbody