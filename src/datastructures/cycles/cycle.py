class Cycle:
    """
    A Class representing a cycle of nodes

    Attributes:
    -----------
    __path : list[int]
        The list of ID's of the nodes that form the cycle

    Methods:
    --------
    get_path() -> list[int]
        Returns __path
    """


    def __init__(self, path:list[int]) -> None:
        """
        Sets up the cycle of the ID's and sorts them

        Parameter:
        ----------
        path : list[int]
            The list of Node ID's that constitute a circle
        """

        self.__path = path
        self.__shuffle_path_start()
        return None
    
    def __shuffle_path_start(self) -> None:
        """
        Changes the start so __path starts with the lowest ID without changing the order of ID's
        """

        min_idx = 0
        min_id = self.__path[0]
        for idx, id in enumerate(self.__path):
            if id < min_id:
                min_id = id
                min_idx = idx
        before = self.__path[:min_idx]
        after = self.__path[min_idx:]
        self.__path = after + before 
        return None

    def __eq__(self, other) -> bool:
        """
        Testing for equality

        Parameters:
        -----------
        other : Any
            Object to test equality against
        """

        if other == None or not isinstance(other, Cycle):
            return False
        
        return self.__path == other.__path
        
    def __hash__(self) -> int:
        """
        Returns the hash of the cycle
        """

        return hash(tuple(self.__path))
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the cycle
        """
        return f"({",".join(map(str, self.__path))})"
    
    def get_path(self) -> list[int]:
        """
        Returns __path
        """
        
        return self.__path
        


def main() -> int:
    print("Calling main function in cycle")
    return 0


if __name__ == "__main__":
    main()