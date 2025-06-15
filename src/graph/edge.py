class Edge:
    def __init__(self, start_id:int, end_id:int) -> None:
        self.__start_id = start_id
        self.__end_id = end_id
        return None
    
    def get_start_id(self) -> int:
        return self.__start_id
    
    def get_end_id(self) -> int:
        return self.__end_id

    def __hash__(self) -> int:
        edge_tuple = (self.__start_id, self.__end_id)
        return hash(edge_tuple)
    
    def __eq__(self, other) -> bool:
        if other == None or not isinstance(other, Edge):
            return False
        return self.__start_id == other.__start_id and self.__end_id == other.__end_id
    
    def __repr__(self) -> str:
        return f"(start:{self.__start_id}|end:{self.__end_id})"
    

def main() -> int:
    print("Calling main function in edge")
    return 0


if __name__ == "__main__":
    main()

