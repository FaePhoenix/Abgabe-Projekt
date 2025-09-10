from datastructures.graph.node import Node
from datastructures.graph.edge import Edge
from datastructures.cycles.cycle import Cycle

class Graph:
    """
    A class representing a directed graph of nodes

    Attributes:
    -----------
    __root : str
        The name of the start-article of the graph

    __nodes : dict[int, Node]
        A map from the ID's to the associated nodes

    __edges : dict[(int, int), Edge]
        A map from the ID tuples to the associated edges

    Methods:
    --------
    calculate_cycles() -> set[Cycle]
        Calculating all cycles/strongly connected components

    get_root() -> str
        Returns the name of the starting article

    get_nodes() -> set[Nodes]
        Returns the nodes as a set

    get_edge() -> set[Edge]
        Returns the edges as a set

    get_density() -> float
        Returns the density of the graph

    get_node_count() -> int
        Returns the amount of nodes in the graph

    get_neighbours(node_id : int) -> list[Node]
        Returns a list of all nodes that are directly connected to the node with the ID node_id

    get_node_with_highest_in() -> Node
        Returns the node with the highest amount of incoming edges

    get_node_with_highest_out() -> Node
        Returns the node with the highest amount of outgoing edges

    get_node_from_id(id : int) -> Node
        Returns the node with ID id

    get_node_name(id : int) -> str
        Returns the name of the node with ID id
    """


    def __init__(self, root:str, nodes:set[Node], edges:set[Edge]) -> None:
        """
        Sets up the graph object by converting the sets of nodes and edges into the maps and calculating information about the interconnectivity and saving it directly into the nodes

        Parameters:
        -----------
        root: str
            The Name of the article that is the root of the graph
        nodes : set[Node]
            The nodes of the graph

        edges : set[Edge]
            The edges of the graph
        """
        self.__root:str = root
        self.__nodes:dict[int, Node] = { node.get_id() : node for node in nodes}
        self.__edges:dict[tuple[int, int], Edge] = {(edge.get_start_id(), edge.get_end_id()) : edge for edge in edges}
        self.__extend_nodes()
        return None
    
    
    def calculate_cycles(self) -> set[Cycle]: # TODO
        """
        Calculates all directed Cycles in the graph
        """

        return set()   

    def __extend_nodes(self) -> None:

        for edge in self.__edges.values():
            start_id = edge.get_start_id()
            end_id = edge.get_end_id()

            start = self.get_node_from_id(start_id)
            assert isinstance(start, Node)
            start.add_outgoing(edge)

            end = self.get_node_from_id(end_id)
            assert isinstance(end, Node)
            end.add_incoming(edge)

        return None

    def get_root(self) -> str:
        """
        Returns the name of the root-article
        """
        return self.__root

    def get_nodes(self) -> set[Node]:
        """
        Returns the nodes as a set
        """

        return set(self.__nodes.values())
    
    def get_edges(self) -> set[Edge]:
        """
        Returns the edges as a set
        """

        return set(self.__edges.values())
    
    def get_density(self) -> float:
        """
        Calculates the density of the graph
        """

        node_count = len(self.__nodes)
        edge_count = len(self.__edges)
        return edge_count / (node_count * (node_count - 1))
    
    def get_node_count(self) -> int:
        """
        Returns the amount of nodes in the graph
        """
        return len(self.__nodes)

    def get_neighbours(self, node_id:int) -> list[Node | None]:
        """
        Returns all nodes that are directly connected to the node which ID is node_id

        Parameters:
        -----------
        node_id : int
            The id of the node wich neighbours are looked for
        """

        outgoing_neighbour_ids = [edge.get_end_id() for edge in self.__edges.values() if edge.get_start_id() == node_id]
        incoming_neighbour_ids = [edge.get_start_id() for edge in self.__edges.values() if edge.get_end_id() == node_id]
        neighbour_ids = set(outgoing_neighbour_ids + incoming_neighbour_ids)

        return [self.__nodes.get(neighbour_id) for neighbour_id in neighbour_ids]
    
    def get_node_with_highest_in(self) -> Node:
        """
        Returns the node with the highest amount of incoming edges
        """

        max_in = 0
        max_id = 0
        for node in self.__nodes.values():
            incoming = len(node.get_incoming())
            if incoming > max_in:
                max_in = incoming
                max_id = node.get_id()

        max_in_node = self.__nodes.get(max_id)
        assert max_in_node

        return max_in_node
    
    def get_node_with_highest_out(self) -> Node:
        """
        Returns the node with the highest amount of outgoing edges
        """

        max_out = 0
        max_id = 0
        for node in self.__nodes.values():
            outgoing = len(node.get_outgoing())
            if outgoing > max_out:
                max_out = outgoing
                max_id = node.get_id()

        max_out_node = self.__nodes.get(max_id)
        assert max_out_node

        return max_out_node
    
    def get_node_from_id(self, id:int) -> Node | None:
        """
        Returns the node which ID is id

        Paramters:
        ----------
        id : int
            The id of the node that is being looked for
        """
        return self.__nodes.get(id)

    def get_node_name(self, id:int) -> str | None:
        """
        Returns the name of the node which ID is id if it exists

        Parameters:
        -----------
        id : int
            The id of the node which name is being looked for
        """
        
        node = self.get_node_from_id(id)

        if not node:
            return None
        
        return node.get_name()
    
    def get_node_id_from_name(self, name:str) -> int | None:
        """
        Returns the id of the node which name matches the provided if it exists

        Parameters:
        -----------
        name : str
            The name of the node which id is being looked for
        """

        for node in self.__nodes.values():
            if node.get_name() == name:
                return node.get_id()
            
        return None


def main() -> int:
    print("Calling main function in graph")
    return 0


if __name__ == "__main__":
    main()