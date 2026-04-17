#/actual_version : 1.2.3
#/TODO Add configuration for custom shortcut aliases and CLI help text
#/file_intro
"""
This module exposes the CLI argument configuration and supported language,
format, and truthy/falsy option values used by the EasyDoc interactive and
non-interactive entry points.
"""


#/const SHORT_CUT_ARGS defines the shortcut argument allowed in the CLI and their corresponding full argument name. For example, "rec" is a shortcut for "recursive", "of" for "onefile", "lang" for "language", "f" for "format", and "rec_d" for "recursive_depth".
SHORT_CUT_ARGS = {"rec" : "recursive", "of" : "onefile", "lang" : "language", "f" : "format", "rec_d" : "recursive_depth"}

#/const AUTHORIZED_ARGS defines the list of all the authorized arguments that can be used in the CLI, either with their full name or their shortcut. This includes "path", "type", "format", "recursive", "onefile", "language", "main", and "recursive_depth".
AUTHORIZED_ARGS = ["path", "type", "format", "recursive", "onefile", "language", "main", "recursive_depth"]

#/const LANGUAGES defines the supported languages for documentation generation, which include "fr" (French), "en" (English), and "jp" (Japanese).
LANGUAGES = ["fr", "en", "jp"]

#/const FORMATS defines the supported documentation formats that can be generated.
FORMATS = ["md", "html"]

#/const TYPES defines the supported types of documentation treatment.
TYPES = ["file", "dir"]

#/const YES_ANSWERS defines the list of truthy responses that can be used in the CLI for boolean arguments.
YES_ANSWERS = ["y", "yes", "1", "true"]
#/const NO_ANSWERS defines the list of falsy responses that can be used in the CLI for boolean arguments.
NO_ANSWERS = ["n", "no", "0", "false"]