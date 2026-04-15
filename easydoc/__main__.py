from argparse import ArgumentParser
from importlib.metadata import version
import pathlib

from .main_manager import Parser
from .classes import NotDeveloppedError


parser = ArgumentParser()
parser.add_argument("-v", "--version", 
                    action="store_true", 
                    help="show the version of EasyDocPy and exit")
parser.add_argument("-type", 
                    choices=["file", "dir"], 
                    help="the type of document to treat, either a single file or a whole directory")
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


path = pathlib.Path(args.path)

if not path.exists() : 
    raise ValueError(f"Invalid path: The path {args.path} doesn't exists")

match args.type :

    case "file":
        if path.suffix != ".py" : 
            raise ValueError(f"Invalid path: The path {args.path} doesn't point to a python file")
        Parser(path)
    case "dir":
        raise NotDeveloppedError("the directory documentation mode hasn't been developped yet.")
    case _ :
        raise ValueError("Invalid value for -type. The type of document to treat must be either 'file' or 'dir'")