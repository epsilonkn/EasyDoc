# Doc

**Welcome to the page of the EasyDoc project**

The idea of that package is to create a technical documentation of a python source file, from the docstrings and the commentary in the source code : yes, the more you comment your code, the more the module will scrap.

## To use it : 

### Command Line :

Here is the only way implemented to generate a documentation in command line :

    easydoc file "/your/path/to/file.py"

Note 1 : your terminal must be in the directory where you want to see the documentation generated.

Note 2 : you can pass the path without double quotes, however it is better to keep them if your path got spaces in it.

### in a python program

Disclaimer : Running the module in a program by calling directly the classes can be possible, but this might also opens a pandora box of bugs.

The reason you would need to run the module manually in a python file is to get a better control over the process.
Unfortunately, in the actual state of the module, the control over the module is still very little, this will be improved in the next updates.

If you still wish to do it in a program rather than in command line, here is the base :

    From easydoc import Parser, Generator

    parser = Parser(path = "/path/to/file.py", automatic = False)
    parse_list = parser.get_parse()
    file_header = parser.get_intro()

    Generator.run(parse_list, file_header, doc_file_name)



## Next updates :

|Version | Improvement|
|-|-|
|V 1.2.0 | adding custom comment line to add info to the documentation|
|V 1.3.0| better control over the process when done in a program |
|V 1.4.0| adding doc generation for an entire directory |
|......||

## API :

The API is still very small, for now, you can just generate manually the documentation.
\
You can also access the class attribute "markdown" which is the base used for the generation.