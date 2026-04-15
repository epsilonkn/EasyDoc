import sys
from .analyser import Parser
from .exceptions import NotDeveloppedError
import pathlib
from argparse import ArgumentParser

from importlib.metadata import version

parser = ArgumentParser()
parser.add_argument("-v", "--version", 
                    action="store_true", 
                    help="show the version of PyEasyDoc and exit")
parser.add_argument("type", 
                    choices=["file", "dir"], 
                    help="the type of document to treat, either a single file or a whole directory")
parser.add_argument("path", 
                    help="the path to the file or directory to document")

args = parser.parse_args()

if args.version:
    print("PyEasyDoc", version("PyEasyDoc"))
    exit(0)

path = pathlib.Path(args.path)

if not path.exists() : 
    raise ValueError(f"The path {args.path} is doesn't exists")

match args.type :

    case "file":
        if path.suffix != ".py" : 
            raise ValueError(f"The path {args.path} doesn't point to a python file")
        Parser(path)
    case "dir":
        if path.suffix != ".py" : 
            raise NotDeveloppedError("the directory documentation mode hasn't been developped yet.")