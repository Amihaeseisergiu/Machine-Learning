class Node:
   
    def __init__(self, label, comm):
        self.label = label
        self.children = {}
        self.mostCommon = comm
        self.parent = None
        self.branchValue = None
        self.pruned = False
        self.continuous = False
        self.splitAttr = None
    
