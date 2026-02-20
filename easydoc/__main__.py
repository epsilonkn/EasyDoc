import sys
import analyser
import pathlib

types = ["file", "dir"]

if sys.argv[1] not in types : 
    raise ValueError(f"The parameter {sys.argv[1]} is invalid\neasydoc accepts only \"file\" and \"dir\"")

path = pathlib.Path(sys.argv[2])

if not path.exists() : 
    raise ValueError(f"The path {sys.argv[1]} is doesn't exists")

match sys.argv[1] :

    case "file":
        if not path.suffix != ".py" : 
            raise ValueError(f"The path {sys.argv[1]} doesn't point to a python file")
        analyser.Parser(sys.argv[1])
    case "group":
        if not path.suffix != ".py" : 
            raise NotImplementedError("the directory documentation mode hasn't been developped yet.")