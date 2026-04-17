import os
from pathlib import Path

from easydoc.classes import Parsed_file, Custom_comment, Parsed_function, Parsed_class, Node, Leaf
from easydoc.generators import OneFileMdGenerator, DirMdGenerator

from easydoc.main_manager import Parser

class TreatmentManager:
    
    def __init__(self, path: str, type: str, format: str, recursive: bool = False, onefile: bool = False, main: str = None, debug: bool = False) -> None:
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
        self.path = path
        self.type = type
        self.format = format
        self.recursive = recursive
        self.onefile = onefile
        self.main_file = main
        self.debug = debug

        match self.type :
            case "file":
                if self.debug:
                    print(f"[DEBUG] [TreatmentManager] Treating the file : {self.path}")
                self._treat_file()
            case "dir":
                if self.debug:
                    print(f"[DEBUG] [TreatmentManager] Treating the directory : {self.path}")
                self._treat_dir()

    
    @staticmethod
    def get_default_args():
        return {
            "path": "",
            "type": "",
            "format": "",
            "recursive": False,
            "onefile": False,
            "main": ""
        }
            

    def _parse_file(self, path: str) -> tuple[list[Parsed_class, Parsed_function], list[Custom_comment]]:
        """Treat a single file and generate its documentation"""
        if Path(path).suffix != ".py":
            raise ValueError(f"The path {path} is not a Python file")   
        parser = Parser(path, debug=self.debug)
        content_list = parser.get_parse()
        file_data = parser.get_file_data()
        return content_list, file_data


    def _search_file(self, path: str, parent : Node | None = None) -> Node:
        if os.path.isdir(path):
            root = Node(os.path.basename(path), path = path, parent = parent)
            for file in os.listdir(path):

                if os.path.isdir(os.path.join(path, file)) and self.recursive:
                    if self.debug:
                        print(f"[DEBUG] [TreatmentManager] Walking into the subdirectory : {(root / file).full_path}")
                    root.add_child(self._search_file(os.path.join(path, file), root))

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
        


if __name__ == "__main__":
    node = TreatmentManager("easydoc", "dir", "md", recursive=True, onefile=True, main="main.py", debug=True)._search_file("easydoc")
    assert type(node) == Node
    assert node.name == "easydoc"
    node.show_tree()