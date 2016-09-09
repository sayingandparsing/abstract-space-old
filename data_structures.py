class Node:
    """"""
    def __init__(self):
        self.descendants = {}
        self.parent = None
        self.name = None
        self.symbol = None

    def get_parent(self):
        pass

    def get_path(self):
        p = self.get_parent()
        if p is not None:
            p.get_path()
        else:
            return self.symbol


class CommandNode(Node):
    def __init__(self):
        super(CommandNode, self).__init__()
        self.command = None


class BranchingNode(Node):
    def __init__(self):
        super(BranchingNode, self).__init__()
        pass


class Tree:
    """"""
    def __init__(self, root_node: BranchingNode):
        self.root_node = root_node
        self.current_node = self.root_node

    def backtrack(self):
        pass

    def get_current(self):
        pass

    def get_descendants(self):
        pass




class DirectoryNode(Node):
    """"""
    def __init__(self, path):
        super(DirectoryNode, self).__init__()
        self.path = path

