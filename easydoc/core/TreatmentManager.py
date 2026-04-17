import os
from pathlib import Path

from easydoc.classes import Parsed_file, Custom_comment, Parsed_function, Parsed_class, Node, Leaf
from easydoc.generators import OneFileMdGenerator, DirMdGenerator

from easydoc.core import Parser

class TreatmentManager:
    
    def __init__(self, **kwargs) -> None:
        """
        Initialize the treatment and generation of a documentation

        Args:
            path (str): path to the file or directory to document
            type (str): type of document to treat, either "file" or "dir"
            format (str): format of the documentation to generate
            recursive (bool): whether to search for Python files recursively in the directory
            onefile (bool): whether to generate a single documentation file for the whole directory
            main (str): path to the main file for the directory
            debug (bool): whether to enable debug mode
        """
        self.path = kwargs.pop("path", None)
        assert self.path is not None, "The path argument is required"
        self.type = kwargs.pop("type", "file")
        self.format = kwargs.pop("format", "md")
        self.recursive = kwargs.pop("recursive", False)
        self.recursive_depth = kwargs.pop("recursive_depth", 0)
        self.onefile = kwargs.pop("onefile", False)
        self.main_file = kwargs.pop("main", None)
        self.debug = kwargs.pop("debug", False)

        if len(kwargs) > 0:
            print(f"[Warning] the following arguments are not recognized : {', '.join(kwargs.keys())}")

        match self.type :
            case "file":
                if self.debug:
                    print(f"[DEBUG] [TreatmentManager] Treating the file : {self.path}")
                self._treat_file()
            case "dir":
                if self.debug:
                    print(f"[DEBUG] [TreatmentManager] Treating the directory : {self.path}")
                self._treat_dir()
            

    def _parse_file(self, path: str) -> tuple[list[Parsed_class, Parsed_function], list[Custom_comment]]:
        """Treat a single file and generate its documentation"""
        if Path(path).suffix != ".py":
            raise ValueError(f"The path {path} is not a Python file")   
        parser = Parser(path, debug=self.debug)
        content_list = parser.get_parse()
        file_data = parser.get_file_data()
        return content_list, file_data


    def _search_file(self, path: str, parent : Node | None = None, depth: int = 0) -> Node:
        if os.path.isdir(path):
            root = Node(os.path.basename(path), path = path, parent = parent)
            for file in os.listdir(path):

                if os.path.isdir(os.path.join(path, file)) and self.recursive and depth < self.recursive_depth:
                    if self.debug:
                        print(f"[DEBUG] [TreatmentManager] Walking into the subdirectory : {(root / file).full_path}")
                    root.add_child(self._search_file(os.path.join(path, file), root, depth + 1))

                elif file.endswith(".py"):
                    if self.debug:
                        print(f"[DEBUG] [TreatmentManager] Treating the file : {(root / file).full_path}")
                    leaf = root / Leaf(file)
                    leaf.associated_parse = Parsed_file(leaf.full_path, *self._parse_file(os.path.join(path, file)))

            return root
        else :
            raise ValueError(f"The path {path} is not a directory")


    def _treat_file(self, path: str = None):
        """Treat a single file and generate its documentation"""
        if path is None:
            path = self.path
        content, data = self._parse_file(path)
        OneFileMdGenerator(content, data, Path(path).stem, debug = self.debug)


    def _treat_dir(self):

        """Treat a whole directory and generate the documentation for all the files in it"""
        if self.debug:
            print(f"[DEBUG] [TreatmentManager] Searching for Python files in the directory : {self.path}")
            print(f"[DEBUG] [TreatmentManager] Using recursive search : {self.recursive}")

        tree : Node[Leaf, Node] = self._search_file(self.path)

        if self.debug:
            print(f"[DEBUG] [TreatmentManager] Found {len([file for file in tree if isinstance(file, Leaf)])} Python files in the directory : {self.path}")
            tree.show_tree()

        for file in tree:
            if not self.onefile and isinstance(file, Leaf):
                if self.debug:
                    print(f"[DEBUG] [TreatmentManager] Treating the file : {file}")
                self._treat_file(file.full_path)
        if self.onefile :
            if self.debug:
                print(f"[DEBUG] [TreatmentManager] Generating a single documentation file for the whole directory : {self.path}")
            DirMdGenerator(list(tree), 
                           dirname=Path(self.path).stem, 
                           main = self.main_file,
                           debug=self.debug)