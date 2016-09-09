from .data_structures import Tree, BranchingNode, CommandNode, Node
from collections import namedtuple
import typing
if typing.TYPE_CHECKING:
    from typing import Dict



class TreeFromNestedDict:
    """
    This class is used to convert from the nested dict format
    specified in the config, to a linked-list based tree structure.

    The input is traversed and reconstructed depth-first through
    recursive calls to the traverse method.
    """
    def __init__(self, nested: Dict[str, dict]):
        #self.lab_ref = namedtuple('LabeledReference', ['label', 'node_ref'])
        self.root_node = self.traverse(nested)  # type: Node

    def traverse(self, nested_dict) -> Node:
        node = self.construct_node(nested_dict)
        if isinstance(node, CommandNode):
            return node
        for key in nested_dict.keys():
            print(key)
            subdict = nested_dict[key]
            ref = self.traverse(subdict)
            #link = self.lab_ref(ref.name, ref)
            link = (ref.name, ref)
            node.descendants[key] = link
        return node

    def construct_node(self, adict) -> Node:
        data = {'name': adict.pop('name', None),
                'cmd': adict.pop('cmd', None)}
        if self.is_branching(data):
            node = BranchingNode()
            if data['name'] is not None:
                node.name = data['name']
            else:
                node.name = 'unnamed'
        else:
            node = CommandNode()
            node.command = data['cmd']
            if data['name'] is not None:
                node.name = data['name']
            else:
                node.name = data['cmd']
        return node

    @staticmethod
    def is_branching(data: dict) -> bool:
        if data['cmd'] is None:
            return True
        else:
            return False


