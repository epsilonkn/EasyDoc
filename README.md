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


#### Generate the documentation :

### In a terminal :

Here is the only way implemented to generate a documentation in command line :

    easydoc file "/your/path/to/file.py"

Note 1 : your terminal must be in the directory where you want to see the documentation generated.

Note 2 : you can pass the path without double quotes, however it is better to keep them if your path got spaces in it.

### In a python program :

Not implemented yet, you'll have to wait for the V1.3.0


## Next updates :

|Version | Improvement|
|-|-|
|V 1.2.0 | adding custom comment line to add info to the documentation|
|V 1.3.0| better control over the process when done in a program |
|V 1.4.0| adding doc generation for an entire directory |
|V 1.5.0| adding user configuration |
|......||

## API :

For now there is no released API entry points in the module, you'll have to wait for the V1.3 and V1.5 for these parts
