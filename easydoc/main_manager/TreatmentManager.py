import os
from pathlib import Path

from easydoc.generators import MarkdownGenerator

from .FileParser import Parser

class TreatmentManager:
    
    def __init__(self, path: str, type: str, format: str) -> None:
        """
        Initialize the treatment and generation of a documentation

        Args:
            path (str): path to the file or directory to document
            type (str): type of document to treat, either "file" or "dir"
            format (str): format of the documentation to generate
        """
        self.path = path
        self.type = type
        self.format = format
        self.recursive = False

        match self.type :
            case "file":
                self._treat_file()
            case "dir":
                self._treat_dir()
            


    def _parse_file(self):
        """Treat a single file and generate its documentation"""
        parser = Parser(self.path)
        content_list = parser.get_parse()
        file_data = parser.get_file_data()
        return content_list, file_data


    def _search_file(self, path: str, py_f_list: list[str] = []):
        if os.path.isdir(path):
            for file in os.listdir(path):
                if os.path.isdir(path) and self.recursive:
                    self._search_file(os.path.join(path, file), py_f_list)
                elif path.endswith(".py"):
                    py_f_list.append(path) 
        elif path.endswith(".py"):
            py_f_list.append(path)

    
    def _treat_file(self):
        """Treat a single file and generate its documentation"""
        content, data = self._parse_file()
        MarkdownGenerator(content, data, Path(self.path).stem)



    def _treat_dir(self):
        """Treat a whole directory and generate the documentation for all the files in it"""
        py_files = []
        self._search_file(self.path, py_files)
        for file in py_files:
            self._treat_file(file)
