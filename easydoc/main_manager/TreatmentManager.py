import os
from pathlib import Path

from easydoc.classes import Custom_comment, Parsed_function, Parsed_class
from easydoc.generators import MarkdownGenerator

from .FileParser import Parser

class TreatmentManager:
    
    def __init__(self, path: str, type: str, format: str, recursive: bool = False, onefile: bool = False) -> None:
        """
        Initialize the treatment and generation of a documentation

        Args:
            path (str): path to the file or directory to document
            type (str): type of document to treat, either "file" or "dir"
            format (str): format of the documentation to generate
            recursive (bool): whether to search for Python files recursively in the directory
            onefile (bool): whether to generate a single documentation file for the whole directory
        """
        self.path = path
        self.type = type
        self.format = format
        self.recursive = recursive
        self.onefile = onefile

        match self.type :
            case "file":
                self._treat_file()
            case "dir":
                self._treat_dir()

    
    @staticmethod
    def get_default_args():
        return {
            "path": "",
            "type": "",
            "format": "",
            "recursive": False,
            "onefile": False
        }
            

    def _parse_file(self, path: str) -> tuple[list[Parsed_class, Parsed_function], list[Custom_comment]]:
        """Treat a single file and generate its documentation"""
        parser = Parser(path)
        content_list = parser.get_parse()
        file_data = parser.get_file_data()
        return content_list, file_data


    def _search_file(self, path: str, py_f_list: list[str] = []):
        if os.path.isdir(path):
            for file in os.listdir(path):
                print(file, file.endswith(".py"))
                if os.path.isdir(os.path.join(path, file)) and self.recursive:
                    self._search_file(os.path.join(path, file), py_f_list)
                elif file.endswith(".py"):
                    print("append")
                    py_f_list.append(os.path.join(path, file)) 
        elif path.endswith(".py"):
            py_f_list.append(path)

    
    def _treat_file(self, path: str = None):
        """Treat a single file and generate its documentation"""
        if path is None:
            path = self.path
        content, data = self._parse_file(path)
        MarkdownGenerator(content, data, Path(path).stem)


    def _treat_dir(self):
        """Treat a whole directory and generate the documentation for all the files in it"""
        py_files = []
        self._search_file(self.path, py_files)
        print(py_files)
        for file in py_files:
            self._treat_file(file)
