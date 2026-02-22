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
from importlib.resources import files


class MarkdownGenerator:

    def __init__(self, obj_list, intro, fname):
        body : str = self.open_pattern()
        body = body.replace("%intro%", intro)
        body = body.replace("%nom_module%", fname)
        for elt in obj_list :
            if isinstance(elt, Parsed_class):
                body += self.generate_class(elt)

        for elt in obj_list :
            if isinstance(elt, Parsed_function):
                body += self.generate_function(elt)

        self.create_file(fname, body)


    # --------------- default wrapper functions ------------------


    @staticmethod
    def _class_wrap(name) : 
        return f"\n### Classe {name} :\n---\n"
    @staticmethod
    def _method_wrap(name) : 
        return f"\n#### **Methode {name} :**\n"
    @staticmethod
    def _function_wrap(name) : 
        return f"\n### Fonction {name} :\n"
    @staticmethod
    def _main_name_wrap(name) : 
        return f"\n### Fonction {name} :\n"
    

    # --------------- hook functions ------------------


    @classmethod
    def set_class_wrap(cls, wrapper) : 
        cls._class_wrap = wrapper
        return wrapper
    
    @classmethod
    def set_method_wrap(cls, wrapper) : 
        cls._method_wrap = wrapper
        return wrapper
    
    @classmethod
    def set_function_wrap(cls, wrapper) : 
        cls._function_wrap = wrapper
        return wrapper
    
    @classmethod
    def set_main_name_wrap(cls, wrapper) : 
        cls._main_name_wrap = wrapper
        return wrapper


    # --------------- files related functions ------------------


    @staticmethod
    def open_pattern():
        return files("easydoc.templates").joinpath("template.md").read_text()
        
    
    @staticmethod
    def create_file(name, body):
        with open(f"{os.getcwd()}/{name}_doc.md", 'w', encoding="utf-8") as f:
            return f.write(body)
        

    # --------------- generation functions ------------------


    def generate_class(self, classe : Parsed_class):
        subbody = self._class_wrap(classe.name)
        subbody += f"\nDéclaration :\n\n\t{classe.declaration}"
        subbody += f"\nDescription :\n{classe.docstring}"
        for func in classe.methods:
            subbody += self.generate_function(func, True)

        return subbody


    def generate_function(self, func : Parsed_function, in_class : bool = False):
        if in_class :
            subbody = self._method_wrap(func.name)
        else : 
            subbody = self._function_wrap(func.name)

        
        subbody += f"\nDéclaration :\n\n{func.declaration}"
        if func.docstring:
            subbody += f"\nDescription :\n\n{func.docstring}"

        return subbody