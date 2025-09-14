from datastructures.cycles.cycle import Cycle
from datastructures.cycles.tarjan_graph import TarjanGraph
from datastructures.cycles.tarjan_node import TarjanNode
from datastructures.graph.graph import Graph


class TarjanCalculator:
    """
    A Class to execute Tarjan's algorithm

    Attributes:
    -----------
    __stack : list[int]
        Stack that is being used to keep track of currently explored nodes for the Tarjan algorithm

    __index : int
        Counter for uniquely indexing nodes for Tarjan's algorithm

    __sccs : list[list[int]]
        A list to keep track of strongly connected components that are found during the execution of Tarjan's algorithm

    __graph : TarjanGraph
        The simplified graph for use in Tarjan's algorithm

    Methods:
    --------
    find_strongly_connected_components(graph : Graph) -> set[Cycle]
        Finds all strongly connected components in the given graph and returns them as a set
    """


    def __init__(self) -> None:
        """
        Sets up the object
        """

        self.__stack:list[int]
        self.__index:int
        self.__sccs:list[list[int]]
        self.__graph:TarjanGraph
        return None
     

    def calculate_sccs(self, graph:TarjanGraph, verbose:bool) -> list[list[int]]:
        """
        The Tarjan algorithm

        Parameters:
        -----------
        graph : TarjanGraph
            The graph to be searched
        """

        self.__graph = graph
        self.__index = 0
        self.__stack = []
        self.__sccs = []

        for node in graph.get_nodes():
            if node.get_index() == -1:
                self.__strong_connect(node, verbose)

        if verbose:
            report_statement = '' \
            'Building components done'

            print(report_statement)

        return self.__sccs
    
    def __strong_connect(self, node:TarjanNode, verbose:bool) -> None:
        """
        Recursive function using a depth search to traverse the graph and updating __lowlink of the nodes

        Parameters:
        -----------
        node : TarjanNode
            The node that is currently being epxlored
        """
        if verbose:
            report_statement = '' \
            f'Adding {node.get_id()} to the stack'

            print(report_statement)

        node.set_index(self.__index)
        node.set_lowlink(self.__index)
        self.__index += 1

        self.__stack.append(node.get_id())

        for child_id in node.get_children():
            child = self.__graph.get_node_from_id(child_id)
            assert child
            
            if child.get_index() == -1:
                self.__strong_connect(child, verbose)
                node.set_lowlink(min(node.get_lowlink(), child.get_lowlink()))

            elif child_id in self.__stack:
                node.set_lowlink(min(node.get_lowlink(), child.get_index()))

        if node.get_lowlink() == node.get_index():
            if verbose:
                report_statement = '' \
                'Found strongly connected component.\n' \
                'Building from stack'

                print(report_statement)

            self.__build_scc_from_stack(node.get_id())
        return None
    

    def __build_scc_from_stack(self, scc_start:int) -> None: # REDO
        """
        Build a strongly connected component from the current stack and the given start node

        Parameters:
        -----------
        scc_start : int
            ID of the node that is the start point of the found strongly connected component
        """
        
        scc = []
        while len(self.__stack) > 0:
            node_id = self.__stack.pop(-1)
            scc.append(node_id)
            if node_id == scc_start:
                break
        self.__sccs.append(scc) 
        return None



def main() -> int:
    print("Calling main in tarjan calculator")
    return 0

if __name__ == "__main__":
    main()