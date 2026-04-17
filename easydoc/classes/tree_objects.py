from typing import Union


class Node:
    """Represents a tree node that can contain child nodes and leaves."""

    def __init__(self, name : str, parent : Union["Node", None] = None, path : str = ""):
        """Initialize a tree node.

        Args:
            name (str): The name of the node.
            parent (Union["Node", None]): The parent node, or None for a root node.
            path (str): Optional path string used by the node.
        """
        self.name = name
        self.parent = parent if parent else self
        self.path = path if path else name
        self.children : list[Union["Node", "Leaf"]] = []
        self.root_shown = False


    @property
    def full_path(self) -> str:
        """Return the full path of this node by concatenating parent names."""
        path = self.name
        parent = self.parent
        while parent != parent.parent:
            path = parent.name + "/" + path
            parent = parent.parent
        if self != parent : # if the leaf is not the root
            path = parent.name + "/" + path # includes the root node in the path
        return path
    

    def show_tree(self, level=0):
        """Print the tree structure rooted at this node.

        Args:
            level (int): Current indentation level for recursive display.
        """
        print("\t" * level + "- " + self.name)
        for child in self.children:
            if isinstance(child, Node):
                child.show_tree(level + 1)
            else:
                print("\t" * (level + 1) + "- " + str(child))


    def add_child(self, child : Union["Node", "Leaf"]):
        """Add a child node or leaf to this node.

        Args:
            child (Union["Node", "Leaf"]): Child element to attach.
        """
        self.children.append(child)
        child.parent = self


    def __str__(self):
        """Return the node name."""
        return self.name
    

    def __iter__(self):
        """Iterate over the node and its subtree in depth-first order.

        Yields:
            Union["Node", "Leaf"]: Each node or leaf in the tree.
        """
        if not self.root_shown:
            self.root_shown = True
            yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child
            else:
                yield child
        self.root_shown = False

    
    def __len__(self) -> int:
        """
        returns the sum of all the elements in the tree

        ex :
        root
        ├── child1
        │   ├── child1.1
        │   └── child1.2
        └── child2

        returns 5 for the root node, 3 for child1, 1 for child2 and 1 for the root
        """
        return 1 + sum(len(child) for child in self.children)
 

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
                elt = Leaf(elt)
            else :
                elt = Node(elt)
        if isinstance(elt, Node):
            if elt.name not in [(c := child).name for child in self.children]:
                elt.parent = self
            else :
                print(f"A node with the name {elt.name} already exists in the node {self.name}")
                return c
        elif isinstance(elt, Leaf):
            if elt.name not in [(c := child).name for child in self.children]:
                elt.parent = self
            else :
                print(f"A leaf with the name {elt.name} already exists in the node {self.name}")
                return c
        else:
            raise TypeError(f"Invalid type for element : {type(elt)}. The element must be either a string, a Node or a Leaf.")
        self.add_child(elt)
        return elt


class Leaf:
    """Represents a leaf item in the tree, typically a Python file."""

    def __init__(self, name : str, parent : Union["Node", None] = None):
        """Initialize a tree leaf.

        Args:
            name (str): The name of the leaf.
            parent (Union["Node", None]): The parent node, or None for a detached leaf.
        """
        self.name = name
        self.parent = parent
        self.associated_parse = None


    def __str__(self):
        """Return the leaf name."""
        return self.name
    
    def __len__(self):
        """Return 1 for a leaf."""
        return 1
    
    @staticmethod
    def is_py_leaf(elt : str) -> bool:
        """Return True when the string represents a Python file name.

        Args:
            elt (str): The string to test.

        Returns:
            bool: True when elt ends with .py, False otherwise.
        """
        return elt.endswith(".py")
    
    @property
    def full_path(self) -> str:
        """Return the full path of this leaf by concatenating parent names."""
        path = self.name
        parent = self.parent
        while parent != None and parent != parent.parent:
            path = parent.name + "/" + path
            parent = parent.parent
        if parent != None: # if the leaf is not the root
            path = parent.name + "/" + path # includes the root node in the path
        return path
