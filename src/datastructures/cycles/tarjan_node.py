class TarjanNode:
    """
    A Class representing a node used for calculations in Tarjan's algorithm

    Parameters:
    -----------
    __internal_id : int
        ID of the node for internal association with the original graph
    
    __index : int
        ID for calculations in Tarjan's algorithm

    __lowlink : int
        lowest index of the reachable nodes

    __children : list[int]
        List of internal ID's of all nodes that are directly connected by an edge to this node

    Methods:
    --------
    get_id() -> int
        Returns __internal_id

    get_index() -> int
        Returns __index

    set_index(index : int) -> None
        Sets __index to the given index

    get_lowlink() -> int
        Returns __lowlink

    set_lowlink(lowlink : int) -> None
        Sets __lowlink to the given lowlink

    get_children() -> list[int]
        Returns __children

    """
    def __init__(self, id:int, children:list[int]) -> None:
        """
        Sets up the object given the given internal ID and list of children

        Paramters:
        ----------
        id : int
            The internal ID

        children : list[int]
            The list of ID's of the children
        """

        self.__internal_id:int = id
        self.__index:int = -1
        self.__lowlink:int
        self.__children:list[int] = children
        return None

    def get_id(self) -> int:
        """
        Returns __internal_id
        """

        return self.__internal_id
    
    def get_index(self) -> int:
        """
        Returns __index
        """

        return self.__index
    
    def set_index(self, index:int) -> None:
        """
        Sets __index to the given index

        Parameters:
        -----------
        index : int
            The index to set __index to
        """

        self.__index = index
        return None
    
    def get_lowlink(self) -> int:
        """
        Returns __lowlink
        """
        return self.__lowlink
    
    def set_lowlink(self, lowlink:int) -> None:
        """
        Sets __lowlink to the given lowlink

        Parameters:
        -----------
        lowlink : int
            The lowlink to set __lowlink to
        """

        self.__lowlink = lowlink
        return None
    
    def get_children(self) -> list[int]:
        """
        Returns __children
        """

        return self.__children
    
    def __repr__(self) -> str:
        """
        Returns a printable string of the object
        """
        return f"(ID:{self.__internal_id}, Children:{self.__children})"
    

def main() -> int:
    print("Calling main in tarjan node")
    return 0


if __name__ == "__main__":
    main()