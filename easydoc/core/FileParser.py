#/actual_version : 1.2.3
#/last_release_date : 17/04/2026                          
#/author : Ywan GERARD
#/TODO Add support for more custom comment types and nested declarations
#/file_intro
"""
This module parses Python source code and extracts both standard docstrings
and README-style custom comment markers for documentation generation.
"""


from importlib.resources import files
import json
from pathlib import Path
import re
from easydoc.classes import Parsed_class, Parsed_function, Custom_comment



class Parser:
    """Parse Python source files and extract structured metadata."""

    def __init__(self, path, debug=False) -> None:
        """Initialize the parser and immediately start parsing the file.

        Args:
            path (str): Path to the source file.
            debug (bool): Enable debug logging.
        """
        self.debug = debug
        self.fpath = Path(path)
        self.fname = self.fpath.stem
        self.parse : list[Parsed_class, Parsed_function] = []
        self.customs : dict = self.open_custom_config()
        self.file_data : list[Custom_comment] = []
        self.pointer = 0
        self.parse_source()


    def get_parse(self) -> list[Parsed_class, Parsed_function]:
        """Return parsed classes and functions from the file.

        Returns:
            list[Parsed_class, Parsed_function]: The parsed classes and functions.
        """
        return self.parse
    

    def get_file_data(self) -> list[Custom_comment]:
        """Return the custom comment blocks extracted from the file.

        Returns:
            list[Custom_comment]: The parsed custom comments.
        """
        return self.file_data


    def parse_source(self):
        """Parse the source file and extract classes, functions, and standalone docstrings.

        The standalone docstring in the file is treated as a file-level description.
        """
        source : list[str]= self.get_source()
        if self.debug:
            print(f"[DEBUG] [Parser] Starting to parse the file : {self.fpath}")
        while  self.pointer < len(source):

            if self.is_class(source[self.pointer]): 
                if self.debug:
                    print(f"[DEBUG] [Parser] Found a class declaration at line {self.pointer} : {source[self.pointer]}")
                self.pointer += self.class_parser(source[self.pointer:])
 
            elif self.is_function(source[self.pointer:]): 
                if self.debug:
                    print(f"[DEBUG] [Parser] Found a function declaration at line {self.pointer} : {source[self.pointer]}")
                self.pointer += self.function_parser(source[self.pointer:])

            elif custom:=self.is_custom(source[ self.pointer]) :
                self.pointer += self.parse_custom(custom, source[self.pointer:])

            else :
                self.pointer += 1

    
    def is_custom(self, line : str) -> bool:
        """Detect whether the given line contains a custom comment marker.

        Args:
            line (str): The source line to inspect.

        Returns:
            bool: The custom marker string if found, otherwise False.
        """
        for custom in self.customs:
            if custom in line :
                return custom
        return False
    

    def parse_custom(self, custom : str, lines : list[str]):
        """Parse a custom comment block from the source lines.

        Args:
            custom (str): The custom marker to parse.
            lines (list[str]): The source lines starting at the marker location.

        Returns:
            int: Number of source lines consumed by the custom block.
        """
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
        """Check whether a line declares a class.

        Args:
            line (str): The line to inspect.

        Returns:
            bool: True if the line declares a class, False otherwise.
        """
        return bool(re.search(r"^class\s.*:", line))
    

    def is_function(self, lines : list[str], in_class = False) -> bool:
        """Check whether the current lines start a function declaration.

        This handles both single-line function headers and multi-line headers.

        Args:
            lines (list[str]): The source lines to inspect.
            in_class (bool, optional): Whether the function is indented as a method. Defaults to False.

        Returns:
            bool: True if the lines begin a function declaration, False otherwise.
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
        """Extract a function declaration block from source lines.

        This method returns the full function header and the number of lines consumed.

        Args:
            lines (list[str]): The lines beginning at the function declaration.

        Returns:
            tuple[str, int]: The function declaration string and the number of lines consumed.
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
            return decla, pointer + 1
        if not opened and pointer >= len(lines):
            raise IndexError(f"a parenthesis was opened but never closed on line \n {lines[0]}\nFailed to parse the module")


    def class_parser(self, sub_source : list[str]) -> int: 
        """Parse a class block and extract its docstring and method definitions.

        Args:
            sub_source (list[str]): Source code starting at the class declaration.

        Returns:
            int: Number of lines consumed while parsing the class block.
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
                if self.debug:
                    print(f"[DEBUG] [Parser] Found a method declaration at line {pointer} : {sub_source[pointer]}")
                pointer += self.function_parser(sub_source[pointer:], obj)

            else :
                pointer += 1
        obj.docstring = docstring
        self.parse.append(obj)
        return pointer


    def function_parser(self, sub_source : list[str], parent : Parsed_class = None) -> int:
        """Parse a function or method block and extract its docstring.

        Args:
            sub_source (list[str]): Source code starting at the function declaration.
            parent (Parsed_class, optional): If provided, the function is treated as a method of this class.
                Defaults to None.

        Returns:
            int: Number of lines consumed while parsing the function block.
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
        """Check whether a line begins a multi-line docstring.

        Args:
            line (str): The source line to inspect.

        Returns:
            bool: True if the line starts a multi-line docstring, False otherwise.
        """
        return bool(re.search(r"(?<!')\"{3}", line))
    

    def is_oneline_docstring(self, line: str) -> bool:
        """Check whether a line contains a one-line docstring.

        Args:
            line (str): The source line to inspect.

        Returns:
            bool: True if the line contains a one-line docstring, False otherwise.
        """
        return line.count('"""') == 2


    def format_string(self, string : str) -> str :
        """Format the given string for proper indentation handling.

        This replaces sequences of four spaces with a tab and normalizes tabs.
        If the resulting string has no indentation, a leading tab is added.

        Args:
            string (str): The string to format.

        Returns:
            str: The formatted string.
        """
        string = re.sub(r"\s{4}", "\t", string)
        if "\t" in string :
            nb_tab : str = "\t" * string.count("\t")

            string = string.replace(nb_tab, "\t")
        else :
            string = "\t" + string
        return string


    def get_source(self) -> list[str]:
        """Read and return the source lines of the current file.

        Returns:
            list[str]: Source lines of the file.
        """
        with open(self.fpath, 'r', encoding='utf-8') as f:
            return f.readlines()


    @staticmethod
    def open_custom_config() -> dict:
        """Load the custom comment marker configuration from package resources.

        Returns:
            dict: Loaded configuration for supported custom comment markers.
        """
        with open(files("easydoc.config").joinpath("custom_comment_lines.json"), 'r', encoding='utf-8') as f :
            return json.load(f)