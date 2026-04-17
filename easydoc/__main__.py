from argparse import ArgumentParser
from importlib.metadata import version

from .core import (
    TreatmentManager, 
    InteractiveManager, 
    is_valid_path, 
    TYPES, 
    FORMATS, 
    LANGUAGES
)

parser = ArgumentParser()
parser.add_argument("-v", "--version", 
                    action="store_true", 
                    help="show the version of EasyDocPy and exit")
parser.add_argument("type",
                    nargs="?",
                    choices= TYPES + ["interactive"], 
                    help="the type of document to treat, either a single file or a whole directory, interactive mode allows to set the arguments interactively")
parser.add_argument("-path", 
                    help="the path to the file or directory to document")
parser.add_argument("-f", "--format", 
                    choices=FORMATS,
                    help="the format of the documentation to generate")
parser.add_argument("-l", "--language", 
                    choices=LANGUAGES,
                    help="the language of the documentation to generate")
parser.add_argument("--debug", 
                    default=False,
                    action="store_true",
                    help="enable debug mode")
args = parser.parse_args()

if args.version:
    print("EasyDocPy", version("EasyDocPy"))
    exit(0)



match args.type :
    case "file" | "dir":
        if not is_valid_path(args.path): 
            raise ValueError(f"Invalid path: The path {args.path} doesn't point to a python file")
        TreatmentManager(args.path, args.type, args.format, debug = args.debug)
    case "interactive":
        modif_args = InteractiveManager.run()
        TreatmentManager(**modif_args, debug=args.debug)
    case _ :
        raise ValueError(f"Invalid value for type : {args.type}. The type of document to treat must be  [{', '.join(TYPES)}] or 'interactive'")