import pathlib


class InteractiveManager:


    @staticmethod
    def is_valid_path(path: str) -> bool:
        """Check if the given path is valid and points to a python file or a directory"""
        path = pathlib.Path(path)
        return path.exists() and ((path.is_file() and path.suffix == ".py") or path.is_dir())


    @classmethod
    def run(cls, default_args : dict) -> dict:
        user_answer = ""
        user_answer = input("Enter the type of document to treat (file, dir) :")
        if user_answer not in ["file", "dir"]:
            raise ValueError("Invalid value for document type. The type of document to treat must be either 'file' or 'dir'")
        else :
            default_args["type"] = user_answer.lower().strip()

        user_answer = input("Enter path to the file or directory to document :")
        if not cls.is_valid_path(user_answer):
            raise ValueError("Invalid path. Please enter a valid path to a Python file or directory.")
        else :
            default_args["path"] = user_answer

        while user_answer != "run":
            user_answer = input("Enter 'run' to start the generation, 'help' to see the other options or 'exit' to quit :")
            match user_answer :
                case "help":
                    print("Available options :" )
                    print("\t- run          : start the documentation generation with the current arguments")
                    print("\t- format       : type of documentation to generate, either 'md' or 'html', usage : format = <format>")
                    print("\t- language     : language of the documentation to generate, either 'fr', 'en' or 'jp', usage : NOT IMPLEMENTED") #language = <language>
                    if default_args["type"] == "dir" :
                        print("\t- recursive    : enable or disable the recursive search for python files in the directory, usage : recursive = <y/n>")
                        print("\t- onefile      : generate a single documentation file for the whole directory instead of one file per python file, usage : onefile = <y/n>")
                        print("\t- main         : defines the main file for the directory, usage : main = <file.py> | <subdir/file.py>")
                    print("\t- exit         : quit the program")
                case "run":
                    return default_args
                case "exit":
                    exit(0)
                case _ :
                    if "=" in user_answer :
                        arg, value = user_answer.split("=", 1)
                        arg = arg.strip()
                        value = value.strip()
                        if arg in default_args:
                            if value.lower() in ["y", "yes"]:
                                default_args[arg] = True
                            elif value.lower() in ["n", "no"]:
                                default_args[arg] = False
                            else:
                                default_args[arg] = value
                        else:
                            print(f"Unknown argument: {arg}. Type 'help' to see the available options.")
                    else:
                        print("Invalid command. Type 'help' to see the available options.")