import copy


class QueueEntry:
    """
    A Class to encapsulate the tuple that is an entry in the queue used to build the graph

    Attributes:
    -----------
    __name : str
        The name of the article

    __degree : int
        The amount of times this article has been linked to in the currently explored articles

    __origins : list[int]
        The list of ID's of the explored articles that link to this article

    __depth : int
        The minimum depth that this article has been seen at in the links of the explored articles

    Methods:
    --------
    add_origin(origin_id : int, origin_depth : int) -> None
        Adds a new source to the article and updates __depth if applicable

    get_degree() -> int
        Return __degree

    get_name() -> str
        Returns __name

    get_origins() -> list[int]
        Returns __origins

    get_depth() -> int
        Returns __depth
    """


    def __init__(self, name:str, origin_id:int, depth:int) -> None:
        """
        Sets up the queue entry object, by setting the name and depth, initializing the sources list with the original source and setting the degree to one
        
        Parameters:
        -----------
        name : str
            The name of the article
        
        origin_id : int
            The ID of the explored article that the article was first found to be linked in

        depth : int
            The depth of the source of this article plus one
        """

        self.__name:str = name
        self.__degree:int = 1
        self.__origins:list[int] = [origin_id]
        self.__depth = depth
        return None

    def add_origin(self, origin_id:int, origin_depth:int) -> None:
        """
        Adds a new source to the queue entry and updates the depth if applicable

        Parameters:
        -----------
        origin_id : int
            The ID of the explored article that the article was found to be linked in

        origin depth : int
            The Depth of the explored article that the article was found to be linked in
        """

        self.__degree += 1
        self.__origins.append(origin_id)
        if (origin_depth + 1 < self.__depth):
            self.__depth = origin_depth + 1
        return None

    def get_degree(self) -> int:
        """
        Returns __degree
        """

        return self.__degree
    
    def get_name(self) -> str:
        """
        Returns __name
        """

        return self.__name
    
    def get_origins(self) -> list[int]:
        """
        Returns __origins
        """

        return copy.deepcopy(self.__origins)

    def get_depth(self) -> int:
        """
        Returns __depth
        """
        return self.__depth

def main() -> int:
    print("Calling main function in requester")
    return 0

if __name__ == "__main__":
    main()