#/actual_version : 1.0.0
#/file_intro
"""
This package initializer exports the supported documentation generation classes
for use by the EasyDoc treatment manager.
"""

from .HTMLGenerator import HTMLGenerator
from .MarkdownGenerator import OneFileMdGenerator, DirMdGenerator

__all__ = ["HTMLGenerator", "OneFileMdGenerator", "DirMdGenerator"]