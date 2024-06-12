class FrontierNode:
    def __init__(self, index):
        self.index = index
        self.frontier_nodes_list = []
    
    def checkParentAndChildNode(self, target_node, node_frontier):
        for node in node_frontier:
            for child_node in node.frontier_nodes_list:
                if int(child_node) == int(target_node):
                    node.frontier_nodes_list.remove(child_node)
                    return node.index