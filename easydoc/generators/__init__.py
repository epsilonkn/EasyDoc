#/actual_version : 1.2.3
#/TODO Add generator export metadata and future output types
#/file_intro
"""
This package initializer exports the supported documentation generation classes
for use by the EasyDoc treatment manager.
"""

from .HTMLGenerator import HTMLGenerator
from .MarkdownGenerator import OneFileMdGenerator, DirMdGenerator

__all__ = ["HTMLGenerator", "OneFileMdGenerator", "DirMdGenerator"]