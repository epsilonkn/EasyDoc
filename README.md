# Doc

**Welcome to the page of the EasyDoc project**

The idea of that package is to create a technical documentation of a python source file, from the docstrings and the commentary in the source code : yes, the more you comment your code, the more the module will scrap.

For more information, read the wiki : https://github.com/epsilonkn/EasyDoc/wiki

## Getting Started :

**Using pip :**

    pip install EasyDocPy

**On github :**
\
Read the wiki of the module

## To use it : 

### To comment your code :

#### **declarations :**

Is accepted for classes

    class obj(*parents):

or 

    class obj:

Is accepted for functions :

    def foo(arg, agr2 = 10, arg 3 : str = "poo", *args, **kwargs) -> None :

or 

    def foo(arg, 
            agr2 = 10, 
            arg 3 : str = "poo", 
            *args, 
            **kwargs) -> None :

Note : the tabs before the "def" are obviously accepted, but the module will assume a function with tabs before is a method of a class.

#### **docstrings :**

The docstrings MUST be defined by 3 double quotes at the beginning and same at the end, otherwise it won't work.
\
You can place docstrings below your classes, methods and functions to detail them, they can be juste below the declaration, or some lines below. There can be 1 or multiple docstrings, but they will all get concatenated into one.

Examples : 

    class foo:
        """
        a detail
        """

    class foo:
        """a detail"""

    def foo(*args):
        """
        detail

        args:
            args : detail
        """
    
    def foo(*args):
        """detail"""


#### **custom comment lines :**

To enhance your documentation, there are a few custom comments you can do :

**#/actual_version**
\
Define the version of the file

    Use :
    #/actual_version : V.1.9.25

**#/author :**
\
Define the author the file

    Use :
    #/author : epsilonkn

**#/creation_date :**
\
Date of creation of the file

    Use :
    #/creation_date : 01/01/1900

**#/last_release_date :**
\
Last date of release of the file

    Use :
    #/last_release_date : 02/01/1900

**#/TODO :**
\
List all the todo in the file

    Use :
    #/TODO Find time to write the doc
    #/TODO Write the doc when dev is done
    #/TODO Write the doc of this file

**#/planned :**
\
List all the planned future versions

    Use :
    #/planned V2 : rewrite the code for better scalability
    #/planned V2.1 : patch the errors of the new code
    #/planned V2.2 : ......

**#/file_intro :**
\
Marks the begin of the file intro. the file intro follows the same rules as the function's docstrings.

    Use :
    #/file_intro
    """
    this file is meant to provide the result of the operation 2+2
    it takes as a paramter....
    """

**#/const :**
\
Explains a constant in the code. for now, all the constants are written at the begining of the doc no matter if they're class's constants or file's constants.

    Use :
    #/const CONST defines the gravitation force for calculus purposes
    CONST = 10
    #/const DEFAULT defines the default values for the empty strings
    DEFAULT = "VOID"


## Generate the documentation :

### For a file :

To generate a documentation in command line :

    easydoc file "/your/path/to/file.py"

Note 1 : your terminal must be in the directory where you want to see the documentation generated.

Note 2 : you can pass the path without double quotes, however it is better to keep them if your path got spaces in it.


### For a directory :

To generate a documentation in command line :

    easydoc dir "/your/path/to/dir"

Note 1 : your terminal must be in the directory where you want to see the documentation generated.

Note 2 : you can pass the path without double quotes, however it is better to keep them if your path got spaces in it.


### Advanced generation :

You can also choose to generate the documentation interactively :

    easydoc interactive

This way the package will ask you to enter the parameters, here they are :

__mandatory :__

- _type_ : type of document to treat : file | dir
- _path_ : the path to what you want to treat (file or dir)

__optional :__

- _run_ : start the generation
- _help_ : shows all the options and their usage
- _exit_ : close the generation
- _format_ | f : The format of the documentation | HTML implemented in (V1.5)
- _language | lang_ : The language in which to doc is written | NOT IMPLEMENTED YET (V1.6 planned)
- _recursive | rec_ : (dir only) : Enable/disable recursive file search in subdirs
- _recursive_depth | rec_d_ : (dir only) Depth of recursive search, 0 equals to disable the recursive search
- _onefile | of_ : (dir only) If enable, will generate the whole directory doc in a single file instead a doc file per source file 

### Others arguements :

__-v | --version :__ Shows the version of the package and stop the program.

__--debug :__ Start the debug mode for generation, meaning package will print at each step what it's doing.


## Next updates :

|Version | Improvement| Status|
|-|-|-|
|V 1.2.0 | Adding custom comment line to add info to the documentation| Done |
|V 1.3.0| Better control over the process when done in a program | suppressed from the planning |
|V 1.4.0| V 4 : treatment of dirs \ V 1.4.1 : implementing main file usage in the process \ V 1.4.2 - implementing file meta data in onefile dir doc| In test...|
|V 1.5.0| Generating the doc as a html file | |
|V 1.6.0| Translation in differents languages | |
|V 1.?.0| Adding user configuration | |
|......|||
