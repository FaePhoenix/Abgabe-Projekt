from __future__ import annotations
from datastructures.graph.edge import Edge

class Node:
    """
    A class that represents a node

    Attributes:
    -----------
    __id : int
        ID of the node

    __name : str
        Name of the node

    __keywords : list[str]
        The 10 most frequent keywords

    __depth : int
        The linking distance to the starting article

    __in : dict[(int, int), Edge]
        Map from an ID tuple to the corresponsing edge object which lead to this node

    __out : dict[(int, int), Edge]
        Map from an ID tuple to the corresponsing edge object which lead away from this node

    Methods:
    --------
    get_name() -> str
        Returns __name

    get_id() -> int
        Returns __id

    get_depth() -> int
        Returns __depth

    get_keywords() -> list[str]
        Returns __keywords

    get_incoming() -> list[Edge]
        Returns a list of all incoming Edges

    add_incoming(incoming : Edge) -> None
        Adds the incoming edge to __in

    get_outgoing() -> list[Edge]
        Returns a list of all outgoing Edges

    add_outgoing(outgoing : Edge) -> None
        Adds the outgoing edge to __out
    """


    def __init__(self, id:int, name:str, keywords:list[str], depth:int) -> None:
        """
        Sets up the node obejct

        Paramters:
        ----------
        id : int
            ID of the node

        name : str
            The name of the node

        keywords: list[str]
            The list of 10 keywords from the article
        
        depth : int
            The linking distance to the starting article
        """

        self.__id:int = id
        self.__name:str = name
        self.__keywords:list[str] = keywords
        self.__depth:int = depth
        self.__in:dict[tuple[int, int], Edge] = {}
        self.__out:dict[tuple[int, int], Edge] = {}
        return None

    def __hash__(self) -> int:
        """
        Returns the hash of the node
        """

        self_content = (self.__id, self.__name, tuple(self.__keywords), self.__depth)
        return hash(self_content)
    
    def __eq__(self, other) -> bool:
        """
        Tests the node for equality against other

        Parameters:
        -----------
        other : Any
            Object to be tested for equality against the node
        """

        if other == None or not isinstance(other, Node):
            return False
        return self.__id == other.__id
        
    def __repr__(self) -> str:
        """
        Returns the string representation of the node
        """

        return f"(id:{self.__id}| name:{self.__name}| depth:{self.__depth}| keywords:{",".join(self.__keywords)})"
    
    def get_name(self) -> str:
        """
        Returns __name
        """

        return self.__name
    
    def get_id(self) -> int:
        """
        Returns __id
        """

        return self.__id
    
    def get_depth(self) -> int:
        """
        Returns __depth
        """

        return self.__depth
    
    def get_keywords(self) -> list[str]:
        """
        Returns __keywords
        """

        return self.__keywords
    
    def get_incoming(self) -> list[Edge]:
        """
        Returns the list of incoming edges
        """

        return list(self.__in.values())
    
    def add_incoming(self, incoming:Edge) -> None:
        """
        Adds the edge incoming to __in

        Parameters:
        -----------
        incoming : Edge
            The edge to be added to __in 
        """

        self.__in[(incoming.get_start_id(), incoming.get_end_id())] = incoming
        return None
    
    def get_outgoing(self) -> list[Edge]:
        """
        Returns the list of outgoing edges
        """

        return list(self.__out.values())
    
    def add_outgoing(self, outgoing:Edge) -> None:
        """
        Adds the edge outgoing to __out

        Parameters:
        -----------
        outgoing : Edge
            The edge to be added to __out 
        """

        self.__out[(outgoing.get_start_id(), outgoing.get_end_id())] = outgoing
        return None


def main() -> int:
    print("Calling main function in node")
    return 0


if __name__ == "__main__":
    main()