#-----------------------------------------------------------------------------------------
# Fichier : analyser.py
# Version : 1.2
# Dernier changement : 21/02/2026                         
# dernier éditeur : Ywan GERARD
# Créateur : Ywan GERARD
#
#-----------------------------------------------------------------------------------------

import json
import re

from .objects import Parsed_class, Parsed_function, Custom_comment
import os
from importlib.resources import files


class MarkdownGenerator:

    def __init__(self, obj_list, custom_list : list[Custom_comment], fname):
        body : str = self.open_pattern()
        customs = self.open_custom_config()
        custom_done = []
        for elt in custom_list :
            if elt.type_ in custom_done:
                continue
            elif elt.is_list :
                part = self.generate_custom_list(custom_list, elt.type_)
                body = body.replace(elt.ref, part)
                custom_done.append(elt.type_)
            else :
                body = body.replace(elt.ref, f"{self._custom_header_wrap(elt.type_.replace("_"," "))}{elt.content}\n\\")

                custom_done.append(elt.type_)
        
        for elt in customs :
            if customs[elt]["type"] not in custom_done :
                print(customs[elt]["ref"])
                body = body.replace(f"{customs[elt]["ref"]}\n", "")

        for elt in obj_list :
            if isinstance(elt, Parsed_class):
                body += self.generate_class(elt)

        for elt in obj_list :
            if isinstance(elt, Parsed_function):
                body += self.generate_function(elt)

        body = re.sub(r"\\\n[^a-zA-Z]*\n", "\n", body)

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
    @staticmethod
    def _custom_list_wrap(name) : 
        return f"\n### {name} :\n"
    @staticmethod
    def _custom_header_wrap(name) : 
        return f"**{name}**\n"
    

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
    def open_custom_config() -> dict:
        with open(files("easydoc.config").joinpath("custom_comment_lines.json"), 'r', encoding='utf-8') as f :
            return json.load(f)
    
    
    @staticmethod
    def create_file(name, body):
        with open(f"{os.getcwd()}/{name}_doc.md", 'w', encoding="utf-8") as f:
            return f.write(body)
        

    # --------------- generation functions ------------------


    def generate_custom_list(self, customs : list[Custom_comment], type_):
        md = self._custom_list_wrap(type_)
        elem_list = [cust for cust in customs if cust.type_ == type_]
        for elem in elem_list:
            md += elem.content + "\n\\\n"
        return md
    


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