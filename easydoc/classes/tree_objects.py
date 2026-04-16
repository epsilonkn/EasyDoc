from typing import Union

class Node:

    def __init__(self, name : str, parent : Union["Node", None] = None, path : str = ""):
        self.name = name
        self.parent = parent if parent else self
        self.path = path if path else name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def full_path(self) -> str:
        """
        return the full path of the leaf by concatenating the name of the leaf and the name of its parent nodes
        """
        path = self.name
        parent = self.parent
        while parent != parent.parent:
            path = parent.name + "/" + path
            parent = parent.parent
        path = parent.name + "/" + path # includes the root node in the path
        return path
    
    def __str__(self):
        return self.name
    
    def __iter__(self):
        return iter(self.children)
    
    def __len__(self) -> int:
        """
        returns the sum of all the elements in the tree

        ex :
        root
        ├── child1
        │   ├── child1.1
        │   └── child1.2
        └── child2

        returns 5 for the root node, 3 for child1 and 1 for child2
        """
        return 1 + sum(len(child) for child in self.children)
    
    def show_tree(self, level=0):
        print("\t" * level + "- " + self.name)
        for child in self.children:
            if isinstance(child, Node):
                child.show_tree(level + 1)
            else:
                print("\t" * (level + 1) + "- " + str(child))
    

    def __truediv__(self, elt : Union["Node", "Leaf", str]) -> Union["Node", "Leaf"]:
        """
        Allows to create a path by using the division operator, for example :
        
        root = Node("root")

        root / "child1" / "child1.1"

        will create the following tree :

            root
            └── child1
                └── child1.1

        Args:
            elt (Union["Node", "Leaf", str]): the element to add to the tree, it can be either a string, a Node or a Leaf

        Raises:
            TypeError: Raised when the type of the element is not valid, the element must be either a string, a Node or a Leaf.

        Returns:
            Union["Node", "Leaf"]: returns the created node or leaf
        """
        if isinstance(elt, str):
            if Leaf.is_py_leaf(elt):
                elt = Leaf(elt, self)
            else :
                elt = Node(elt, self)
        elif isinstance(elt, Node):
            elt.parent = self
        elif isinstance(elt, Leaf):
            elt.parent = self
        else:
            raise TypeError(f"Invalid type for element : {type(elt)}. The element must be either a string, a Node or a Leaf.")
        self.add_child(elt)
        return elt


class Leaf:

    def __init__(self, name : str, parent : Union["Node", None] = None):
        self.name = name
        self.parent = parent


    def __str__(self):
        return self.name
    
    def __len__(self):
        return 1
    
    @staticmethod
    def is_py_leaf(elt : str) -> bool:
        """
        return true if the string passed represents a Python file, False otherwise
        """
        if elt.endswith(".py") :
             return True
        
    def full_path(self) -> str:
        """
        return the full path of the leaf by concatenating the name of the leaf and the name of its parent nodes
        """
        path = self.name
        parent = self.parent
        while parent != parent.parent:
            path = parent.name + "/" + path
            parent = parent.parent
        path = parent.name + "/" + path # includes the root node in the path
        return path
        