#/actual_version : 1.0.0
#/TODO Add more reusable utilities for path validation and config discovery
#/file_intro
"""
This module contains small reusable helpers used by the EasyDoc core modules.
"""

import pathlib

def is_valid_path(path: str) -> bool:
    """Check if the given path is valid and points to a python file or a directory."""
    path = pathlib.Path(path)
    return path.exists() and ((path.is_file() and path.suffix == ".py") or path.is_dir())