import pathlib

def is_valid_path(path: str) -> bool:
    """Check if the given path is valid and points to a python file or a directory"""
    path = pathlib.Path(path)
    return path.exists() and ((path.is_file() and path.suffix == ".py") or path.is_dir())