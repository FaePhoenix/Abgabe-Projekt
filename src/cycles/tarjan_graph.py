from cycles.tarjan_node import TarjanNode

class TarjanGraph:
    """
    A class representing a simplified graph for use in the Tarjan algorithm

    Attributes:
    -----------
    __nodes : dict[int, TarjanNode]
        A map of the Nodes in simplified implementation from the internal ID's to the Nodes themselves

    Methods:
    --------
    __init__(nodes : set[TarjanNode]) -> Node
        Sets up __nodes by creating the map using the set of nodes

    get_nodes() -> set[TarjanNode]
        Returns the nodes of the graph as a set

    get_node_from_id(id : int) -> TarjanNode
        Returns the node associated with the given ID
    """


    def __init__(self, nodes:set[TarjanNode]) -> None:
        """
        Sets up __nodes by creating the map using the set of nodes

        Parameters:
        -----------
        nodes : set[TarjanNode]
            The nodes of the graph
        """
        self.__nodes:dict[int, TarjanNode] = {node.get_id() : node for node in nodes}
        return None
    
    def get_nodes(self) -> set[TarjanNode]:
        """
        Returns the nodes as a set
        """

        return set(self.__nodes.values())
    
    def get_node_from_id(self, id:int) -> TarjanNode:
        """
        Returns the node associated with the given ID

        Parameters:
        -----------
        id : int
            The ID of the node
        """

        return self.__nodes.get(id)
    

def main() -> int:
    print("Calling main in tarjan graph")
    return 0


if __name__ == "__main__":
    main()