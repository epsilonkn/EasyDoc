import sys
from .analyser import Parser
import pathlib

types = ["file", "dir"]

if sys.argv[1] not in types : 
    raise ValueError(f"The parameter {sys.argv[1]} is invalid\neasydoc accepts only \"file\" and \"dir\"")

path = pathlib.Path(sys.argv[2])

if not path.exists() : 
    raise ValueError(f"The path {sys.argv[2]} is doesn't exists")

match sys.argv[1] :

    case "file":
        if path.suffix != ".py" : 
            raise ValueError(f"The path {sys.argv[2]} doesn't point to a python file")
        Parser(path)
    case "group":
        if path.suffix != ".py" : 
            raise NotImplementedError("the directory documentation mode hasn't been developped yet.")