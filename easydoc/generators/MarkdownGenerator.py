#-----------------------------------------------------------------------------------------
# Fichier : analyser.py
# Version : 1.2
# Dernier changement : 21/02/2026                         
# dernier éditeur : Ywan GERARD
# Créateur : Ywan GERARD
#
#-----------------------------------------------------------------------------------------

import json
from pathlib import Path
import re

from ..classes import Parsed_class, Parsed_function, Custom_comment, Parsed_file, Leaf, Node
import os
from importlib.resources import files


class MdGenerator:

    def __init__(self, 
                 debug : bool = False):

        self.debug = debug
        if self.debug:
            print(f"[DEBUG] [DirMdGenerator] Opening the template file and the custom comment configuration")
        self.body : str = self.open_pattern()
        self.customs = self.open_custom_config()
        if self.debug:
            print(f"[DEBUG] [DirMdGenerator] Done")
        self.custom_done = []



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
    def _custom_list_wrap(name) : 
        return f"\n### {name} :\n"
    @staticmethod
    def _custom_header_wrap(name) : 
        return f"**{name}**\n"
    @staticmethod
    def _file_wrap(name) : 
        return f"\n## Fichier {name} :\n---\n"
    

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
        if self.debug:
            print(f"[DEBUG] [DirMdGenerator] Generating documentation for the class {classe.name}")
        subbody = self._class_wrap(classe.name)
        subbody += f"\nDéclaration :\n\n\t{classe.declaration}"
        subbody += f"\nDescription :\n{classe.docstring}"
        for func in classe.methods:
            if self.debug:
                print(f"[DEBUG] [DirMdGenerator] Generating documentation for the method {classe.name}.{func.name}")
            subbody += self.generate_function(func, True)

        return subbody


    def generate_function(self, func : Parsed_function, in_class : bool = False):
        if in_class :
            subbody = self._method_wrap(func.name)
        else : 
            if self.debug:
                print(f"[DEBUG] [DirMdGenerator] Generating documentation for the function {func.name}")
            subbody = self._function_wrap(func.name)

        
        subbody += f"\nDéclaration :\n\n{func.declaration}"
        if func.docstring:
            subbody += f"\nDescription :\n\n{func.docstring}"

        return subbody



class OneFileMdGenerator(MdGenerator):

    def __init__(self, obj_list : list[Parsed_class, Parsed_function], custom_list : list[Custom_comment], fname : str, debug : bool = False):

        super().__init__(debug)
        
        self.body = self.body.replace("%module_name%", fname)
        if self.debug :
            print(f"[DEBUG] [DirMdGenerator] Treating the file {fname}")
        for elt in custom_list :
            if elt.type_ in self.custom_done:
                continue
            elif elt.is_list :
                part = self.generate_custom_list(custom_list, elt.type_)
                self.body = self.body.replace(elt.ref, part)
                self.custom_done.append(elt.type_)
            else :
                self.body = self.body.replace(elt.ref, f"{self._custom_header_wrap(elt.type_.replace("_"," "))}{elt.content}\n\\")

                self.custom_done.append(elt.type_)
        
        temp : list[str] = []
        for elt in self.customs :
            if self.customs[elt]["type"] not in self.custom_done :
                temp.append(self.customs[elt]["ref"])
                self.body = self.body.replace(f"{self.customs[elt]["ref"]}\n", "")
        if self.debug and temp :
            print("[DEBUG] [DirMdGenerator] unused customs : ", ", ".join(temp))

        for elt in obj_list :
            if isinstance(elt, Parsed_class):
                self.body += self.generate_class(elt)

        for elt in obj_list :
            if isinstance(elt, Parsed_function):
                self.body += self.generate_function(elt)

        self.body = re.sub(r"\\\n[^a-zA-Z]*\n", "\n", self.body)

        self.create_file(fname, self.body)



class DirMdGenerator(MdGenerator):

    def __init__(self, 
                 file_list : list[Node, Leaf], 
                 dirname : str, 
                 main : str = None,
                 debug : bool = False):

        super().__init__(debug)

        self.body = self.body.replace("%module_name%", dirname)
        self.header_written = False

        for file in file_list :
            if isinstance(file, Node):
                continue
            file : Parsed_file = file.associated_parse
            file_name = Path(file.name).name
            if self.debug :
                print(f"[DEBUG] [DirMdGenerator] Treating the file {file_name}")
            if not self.header_written and (file_name == main or (file_name in ["main.py", "__init__.py" ])):
                if self.debug:
                    print(f"[DEBUG] [DirMdGenerator] Found a main file : {file.name}, writing the header of the documentation with this file")
                self.header_written = True
                for elt in file.file_data :
                    if elt.type_ in self.custom_done:
                        continue
                    elif elt.is_list :
                        part = self.generate_custom_list(file.file_data, elt.type_)
                        self.body = self.body.replace(elt.ref, part)
                        self.custom_done.append(elt.type_)
                    else :
                        self.body = self.body.replace(elt.ref, f"{self._custom_header_wrap(elt.type_.replace("_"," "))}{elt.content}\n\\")

                        self.custom_done.append(elt.type_)
                
                temp : list[str] = []
                for elt in self.customs :
                    if self.customs[elt]["type"] not in self.custom_done :
                        temp.append(self.customs[elt]["ref"])
                        self.body = self.body.replace(f"{self.customs[elt]["ref"]}\n", "")
                if self.debug and temp :
                    print("[DEBUG] [DirMdGenerator] unused customs : ", ", ".join(temp))


            self.body += self._file_wrap(file.name)

            for elt in file.content_list :
                if isinstance(elt, Parsed_class):
                    self.body += self.generate_class(elt)

            for elt in file.content_list :
                if isinstance(elt, Parsed_function):
                    self.body += self.generate_function(elt)

        self.body = re.sub(r"\\\n[^a-zA-Z]*\n", "\n", self.body)

        self.create_file(dirname, self.body)