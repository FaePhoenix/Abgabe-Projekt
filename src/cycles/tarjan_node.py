class TarjanNode:
    def __init__(self, id:int, children:list[int]) -> None:
        self.__internal_id:int = id
        self.__index:int = -1
        self.__lowlink:int
        self.__children:list[int] = children

    def get_id(self) -> int:
        return self.__internal_id
    
    def get_index(self) -> int:
        return self.__index
    
    def set_index(self, index:int) -> None:
        self.__index = index
        return None
    
    def get_lowlink(self) -> int:
        return self.__lowlink
    
    def set_lowlink(self, lowlink:int) -> None:
        self.__lowlink = lowlink
        return None
    
    def get_children(self) -> list[int]:
        return self.__children
    
    def __repr__(self) -> str:
        return f"(ID:{self.__internal_id}, Children:{self.__children})"
    

def main() -> int:
    print("Calling main in tarjan node")
    return 0


if __name__ == "__main__":
    main()