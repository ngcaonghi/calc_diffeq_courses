import diff
import numpy as np
from collections import defaultdict

class BoundExceededError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class BoundedSet(set):
    def __init__(self, *args, **kwarg):
        self.size_limit = kwargs.pop('size_limit', None)
        super().__init__(*args, **kwarg)
        if self.__len__() == self.size_limit:
            raise BoundExceededError('Node only allows', self.size_limit, 'inputs!')
    
    @Override
    def add(self, item):
        if self.__len__() == self.size_limit:
            raise BoundExceededError('Node only allows', self.size_limit, 'inputs!')
        else:
            super().add(item)

class Node(object):
    def __init__(self, nodefunction):
        assert issubclass(nodefunction.__class__, diff.NodeFunction)
        self.function = nodefunction
        self.max_in = self.function.max_in 
        self.input = BoundedSet(size_limit = max_in)
        self.output = set()
    def __repr__(self):
        return self.function.__name
    
        

class Graph:
    '''
    List of functions:
    1. BST traversal to check if graph is DAG
    2. check if the right nodes are deployed 
    '''
    def __init__(self):
        self.V = 

    def 
    