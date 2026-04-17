#/actual_version : 1.2.3
#/TODO Add support for persisted interactive defaults
#/file_intro
"""
This module manages interactive mode input and converts user commands
into the argument dictionary required by TreatmentManager.
"""

from .utils import (
    AUTHORIZED_ARGS, 
    LANGUAGES, 
    FORMATS, 
    SHORT_CUT_ARGS, 
    TYPES, 
    YES_ANSWERS, 
    NO_ANSWERS, 
    is_valid_path
)

class InteractiveManager:
    """Manage the interactive mode.

    Parse user input to set the arguments for the TreatmentManager and start generation.
    """

    @classmethod
    def _ask_type(cls) -> str:
        """
        Ask the user for the document type to treat

        Returns:
            str: returns the document type to treat, either "file" or "dir"
        """
        user_answer = input("Enter the type of document to treat (file, dir) :")
        if user_answer not in TYPES:
            print(f"Invalid value for document type. The type of document to treat must be [{', '.join(TYPES)}].")
            return cls._ask_type()
        return user_answer.lower().strip()
    

    @classmethod
    def _ask_path(cls) -> str:
        """
        Ask the user for the path to the file or directory to document

        Returns:
            str: returns the path to the file or directory to document
        """
        user_answer = input("Enter path to the file or directory to document :")
        if not is_valid_path(user_answer):
            print("Invalid path. Please enter a valid path to a Python file or directory.")
            return cls._ask_path()
        return user_answer


    @classmethod
    def run(cls) -> dict:
        """Start the interactive prompt and return the selected arguments.

        Returns:
            dict: The parsed arguments to pass to TreatmentManager.
        """
        user_answer = ""

        return_args= {}

        return_args["type"] = cls._ask_type()

        return_args["path"] = cls._ask_path()

        while user_answer != "run":
            user_answer = input("Enter 'run' to start the generation, 'help' to see the other options or 'exit' to quit :")
            match user_answer :
                case "help":
                    print("Available options :" )
                    print("\t- run                      : start the documentation generation with the current arguments")
                    print(f"\t- format | f              : type of documentation to generate, either [{', '.join(FORMATS)}], usage : format = <format>")
                    print("\t- language | lang          : language used in the documentation, enter the keyword [language | lang] to see options, usage : NOT IMPLEMENTED") #language = <language>
                    if return_args["type"] == "dir" :
                        print("\t- recursive | rec          : enable or disable the recursive search for python files in the directory, usage : recursive = <y/n>")
                        print("\t- recursive_depth | rec_d  : set the depth of the recursive search for python files in the directory, usage : recursive_depth = <int>")
                        print("\t- onefile | of             : generate a single documentation file for the whole directory instead of one file per python file, usage : onefile = <y/n>")
                        print("\t- main                     : defines the main file for the directory, usage : main = <file.py> | <subdir/file.py>")
                    print("\t- exit                     : quit the program")
                case "language" | "lang":
                    for lang in LANGUAGES:
                        print(f"\t- {lang}")
                case "run":
                    return return_args
                case "exit":
                    exit(0)
                case _ :
                    if "=" in user_answer :
                        arg, value = user_answer.split("=", 1)
                        arg = arg.strip()
                        value = value.strip()
                        if arg in SHORT_CUT_ARGS:
                            arg = SHORT_CUT_ARGS[arg]
                        if arg in AUTHORIZED_ARGS:
                            if value.lower() in YES_ANSWERS:
                                return_args[arg] = True
                            elif value.lower() in NO_ANSWERS:
                                return_args[arg] = False
                            elif arg == "recursive_depth":
                                if value.isdigit() and int(value) >= 0:
                                    return_args[arg] = int(value)
                                else:
                                    print("Invalid value for recursive_depth. It must be a non-negative integer.")
                            else:
                                return_args[arg] = value
                        else:
                            print(f"Unknown argument: {arg}. Type 'help' to see the available options.")
                    else:
                        print("Invalid command. Type 'help' to see the available options.")