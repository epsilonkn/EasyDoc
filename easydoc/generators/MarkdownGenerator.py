#/actual_version : 1.5.0
#/TODO Improve markdown output for nested structures and constants
#/file_intro
"""
This module generates Markdown documentation from parsed EasyDoc file and directory data,
including README-style custom comments and extracted class/function metadata.
"""

import json
from pathlib import Path
import re

from ..classes import Parsed_class, Parsed_function, Custom_comment, Parsed_file, Leaf, Node
import os
from importlib.resources import files


class MdGenerator:
    """Base class for Markdown generators."""

    def __init__(self, 
                 debug : bool = False):
        """Initialize the markdown generator and load the template resources.

        Args:
            debug (bool): Enable debug output during generation.
        """
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
        """Return a markdown header for a class section."""
        return f"\n### Classe {name} :\n---\n"
    @staticmethod
    def _nested_class_wrap(name, parent) : 
        """Return a markdown header for a nested class section."""
        return f"\n### Classe imbriquée {name} dans {parent} :\n---\n"
    @staticmethod
    def _nested_function_wrap(name, parent) : 
        """Return a markdown header for a nested function section."""
        return f"\n#### Fonction imbriquée {name} dans {parent} :\n---\n"
    @staticmethod
    def _method_wrap(name) : 
        """Return a markdown header for a method section."""
        return f"\n#### **Methode {name} :**\n"
    @staticmethod
    def _function_wrap(name) : 
        """Return a markdown header for a function section."""
        return f"\n### Fonction {name} :\n"
    @staticmethod
    def _custom_list_wrap(name) : 
        """Return a markdown header for a custom list section."""
        return f"\n### {name} :\n"
    @staticmethod
    def _custom_header_wrap(name) : 
        """Return a markdown header for a custom comment block."""
        return f"**{name}**\n"
    @staticmethod
    def _file_wrap(name) : 
        """Return a markdown header for a file section."""
        return f"\n## Fichier {name} :\n---\n"
    @staticmethod
    def _custom_wrap(name, value) : 
        """Return a markdown header for a custom comment section."""
        return f"\n{name} : {value}\n \\"
    

    # --------------- files related functions ------------------


    @staticmethod
    def open_pattern():
        """Load the Markdown template pattern for documentation output."""
        return files("easydoc.templates").joinpath("template.md").read_text()
    

    @staticmethod
    def open_custom_config() -> dict:
        """Load custom comment configuration from the package resources."""
        with open(files("easydoc.config").joinpath("custom_comment_lines.json"), 'r', encoding='utf-8') as f :
            return json.load(f)
    
    
    @staticmethod
    def create_file(name, body):
        """Create a documentation file from the generated body.

        Args:
            name (str): Base name of the created documentation file.
            body (str): The content to write.
        """
        with open(f"{os.getcwd()}/{name}_doc.md", 'w', encoding="utf-8") as f:
            f.write(body)
        

    # --------------- generation functions ------------------


    def generate_custom_list(self, customs : list[Custom_comment], title : str):
        """Generate documentation for a list of custom comments.

        Args:
            customs (list[Custom_comment]): Custom comments to render.
            type_ (str): The type of custom comment list to generate.
            title (str): The title for the custom comment list.

        Returns:
            str: The generated markdown block for the custom list.
        """
        md = self._custom_list_wrap(title)
        for elem in customs:
            md += elem.content + "\n\\\n"
        return md
    

    def generate_class(self, classe : Parsed_class, nested : bool = False, parent : str = ""):
        """Generate the markdown block for a parsed class."""
        if self.debug:
            print(f"[DEBUG] [DirMdGenerator] Generating documentation for the class {classe.name}")
        subbody = self._class_wrap(classe.name) if not nested else self._nested_class_wrap(classe.name, parent)
        subbody += f"\nDéclaration :\n\n\t{classe.declaration}"
        subbody += f"\nDescription :\n{classe.docstring}"
        for elem in classe.content :
            if isinstance(elem, Parsed_function):
                if self.debug:
                    print(f"[DEBUG] [DirMdGenerator] Generating documentation for the method {classe.name}.{elem.name}")
                subbody += self.generate_function(elem, in_class = True)
            else :
                if self.debug:
                    print(f"[DEBUG] [DirMdGenerator] Generating documentation for the nested class {classe.name}.{elem.name}")
                subbody += self.generate_class(elem, nested = True, parent = classe.name)
        return subbody


    def generate_function(self, func : Parsed_function, in_class : bool = False, nested : bool = False, parent : str = ""):
        """Generate the markdown block for a parsed function or method."""
        if in_class :
            subbody = self._method_wrap(func.name)
        elif nested :
            if self.debug:
                print(f"[DEBUG] [DirMdGenerator] Generating documentation for the nested function {func.name}")
            subbody = self._nested_function_wrap(func.name, parent)
        else : 
            if self.debug:
                print(f"[DEBUG] [DirMdGenerator] Generating documentation for the function {func.name}")
            subbody = self._function_wrap(func.name)

        
        subbody += f"\nDéclaration :\n\n{func.declaration}"
        if func.docstring:
            subbody += f"\nDescription :\n\n{func.docstring}"

        for elem in func.content :
            if isinstance(elem, Parsed_function):
                if self.debug:
                    print(f"[DEBUG] [DirMdGenerator] Generating documentation for the nested function {func.name} > {elem.name}")
                subbody += self.generate_function(elem, nested = True, parent = func.name)
            else :
                if self.debug:
                    print(f"[DEBUG] [DirMdGenerator] Generating documentation for the nested class {func.name}.{elem.name}")
                subbody += self.generate_class(elem, nested = True, parent = func.name)

        return subbody



class OneFileMdGenerator(MdGenerator):
    """Generate a single markdown documentation file for a list of parsed objects."""

    def __init__(self, fobject : Parsed_file, debug : bool = False):
        """Initialize and generate a documentation markdown file for a single source module.

        Args:
            obj_list (list[Parsed_class, Parsed_function]): Parsed classes and functions.
            custom_list (list[Custom_comment]): Custom comments from the source file.
            fname (str): Base name of the output file.
            debug (bool): Enable debug logging.
        """

        super().__init__(debug)
        
        self.body = self.body.replace("%module_name%", fobject.name)
        if self.debug :
            print(f"[DEBUG] [DirMdGenerator] Treating the file {fobject.name}")
        for elt in fobject.comments :
            if elt.type_ in self.custom_done:
                continue
            elif elt.is_list :
                part = self.generate_custom_list([custom for custom in fobject.comments if custom.type_ == elt.type_], elt.title)
                self.body = self.body.replace(elt.ref, part)
                self.custom_done.append(elt.type_)
            else :
                self.body = self.body.replace(elt.ref, self._custom_wrap(elt.title, elt.content))

                self.custom_done.append(elt.type_)
        
        temp : list[str] = []
        for elt in self.customs :
            if self.customs[elt]["type"] not in self.custom_done :
                temp.append(self.customs[elt]["ref"])
                self.body = self.body.replace(f"{self.customs[elt]["ref"]}\n", "")
        if self.debug and temp :
            print("[DEBUG] [DirMdGenerator] unused customs : ", ", ".join(temp))

        for elt in fobject.content :
            if isinstance(elt, Parsed_class):
                self.body += self.generate_class(elt)

        for elt in fobject.content :
            if isinstance(elt, Parsed_function):
                self.body += self.generate_function(elt)

        self.body = re.sub(r"\\\n[^a-zA-Z]*\n", "\n", self.body)

        self.create_file(fobject.name, self.body)



class DirMdGenerator(MdGenerator):
    """Generate documentation for a directory of Python files."""

    def __init__(self, 
                 file_list : list[Node, Leaf], 
                 dirname : str, 
                 main : str = None,
                 debug : bool = False):
        """Initialize the directory documentation generator.

        Args:
            file_list (list[Node, Leaf]): The file tree nodes and leaves to document.
            dirname (str): The base directory name used for the output file.
            main (str, optional): Optional main file name to use for header selection.
            debug (bool): Enable debug logging.
        """

        super().__init__(debug)

        self.body = self.body.replace("%module_name%", dirname)
        self.header_written = False

        for file in file_list :
            if isinstance(file, Node):
                continue
            file : Parsed_file = file.associated_parse
            parent = str(Path(file.name).parents)
            if self.debug :
                print(f"[DEBUG] [DirMdGenerator] Treating the file {file.name}")
            if not self.header_written and (file.name == main or (file.name in [parent + "/main.py", parent + "/__init__.py", parent + "/__main__.py"])):
                if self.debug:
                    print(f"[DEBUG] [DirMdGenerator] Found a main file : {file.name}, writing the header of the documentation with this file")
                self.header_written = True
                for elt in file.file_data :
                    if elt.type_ in self.custom_done:
                        continue
                    elif elt.is_list :
                        part = self.generate_custom_list([custom for custom in file.file_data if custom.type_ == elt.type_], elt.title)
                        self.body = self.body.replace(elt.ref, part)
                        self.custom_done.append(elt.type_)
                    else :
                        self.body = self.body.replace(elt.ref, self._custom_wrap(elt.title, elt.content))

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