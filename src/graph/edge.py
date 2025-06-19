
class Edge:
    """
    A class representing an edge in a graph

    Attributes:
    -----------
    __start_id : int
        The ID of the node that is the start of the edge

    __end_it : int 
        The ID of the node that is the end of the edge

    Methods:
    --------
    get_start_id() -> int
        Returns __start_id

    get__end_id() -> int
        Returns __end_id
    """


    def __init__(self, start_id:int, end_id:int) -> None:
        """
        Sets up the object

        Parameters:
        -----------
        start_id : int
            ID of the node that is the start of the edge

        end_id : int
            ID of the node that is the end of the edge
        """

        self.__start_id:int = start_id
        self.__end_id:int = end_id
        return None
    
    def get_start_id(self) -> int:
        """
        Returns __start_id
        """

        return self.__start_id
    
    def get_end_id(self) -> int:
        """
        Returns __end_id
        """

        return self.__end_id


    def __hash__(self) -> int:
        """
        Returns the hash of the edge
        """

        edge_tuple = (self.__start_id, self.__end_id)
        return hash(edge_tuple)
    
    def __eq__(self, other) -> bool:
        """
        Tests equality of the edge against other

        Parameters:
        -----------
        other : Any
            Object to be tested for equality against the edge
        """

        if other == None or not isinstance(other, Edge):
            return False
        return self.__start_id == other.__start_id and self.__end_id == other.__end_id
    
    def __repr__(self) -> str:
        """
        Returns the string representation of the edge
        """
        
        return f"(start:{self.__start_id}|end:{self.__end_id})"
    

def main() -> int:
    print("Calling main function in edge")
    return 0


if __name__ == "__main__":
    main()

