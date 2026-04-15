from argparse import ArgumentParser
from importlib.metadata import version
import pathlib

from .classes import NotDeveloppedError

from .main_manager import TreatmentManager, ContextManager


parser = ArgumentParser()
parser.add_argument("-v", "--version", 
                    action="store_true", 
                    help="show the version of EasyDocPy and exit")
parser.add_argument("-type", 
                    choices=["file", "dir", "interactive"], 
                    help="the type of document to treat, either a single file or a whole directory, interactive mode allows to set the arguments interactively")
parser.add_argument("-path", 
                    help="the path to the file or directory to document")
parser.add_argument("-f", "--format", 
                    choices=["md", "html"],
                    help="the format of the documentation to generate")
parser.add_argument("-l", "--language", 
                    choices=["fr", "en", "jp"],
                    help="the language of the documentation to generate")
parser.add_argument("--debug", 
                    action="store_true",
                    help="enable debug mode")
args = parser.parse_args()

if args.version:
    print("EasyDocPy", version("EasyDocPy"))
    exit(0)

def is_valid_path(path: str) -> bool:
    """Check if the given path is valid and points to a python file or a directory"""
    path = pathlib.Path(path)
    return path.exists() and ((path.is_file() and path.suffix == ".py") or path.is_dir())



match args.type :
    case "file" | "dir":
        if not is_valid_path(args.path): 
            raise ValueError(f"Invalid path: The path {args.path} doesn't point to a python file")
        TreatmentManager(args.path, args.type, args.format)
    case "interactive":
        args = ContextManager.run(TreatmentManager.get_default_args())
        TreatmentManager(**args)
    case _ :
        print(args.type)
        raise ValueError("Invalid value for -type. The type of document to treat must be either 'file' or 'dir'")