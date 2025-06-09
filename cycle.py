class Cycle:
    def __init__(self, path:list[int]) -> None:
        self.__path = path
        self.__shuffle_path_start()
        return None
    
    def __shuffle_path_start(self) -> None:
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
        if other == None or not isinstance(other, Cycle):
            return False
        
        return self.__path == other.__path
        
    def __hash__(self) -> int:
        return hash(tuple(self.__path))
    
    def __repr__(self) -> str:
        return f"({",".join(map(str, self.__path))})"
    
    def get_path(self) -> list[int]:
        return self.__path
        


def main() -> int:
    print("Calling main function in cycle")
    return 0


if __name__ == "__main__":
    main()