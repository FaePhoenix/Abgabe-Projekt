import copy


class NodeQueueEntry:
    def __init__(self, name:str, origin_id:int, depth:int) -> None:
        self.__name:str = name
        self.__degree = 1
        self.__origins:list[int] = [origin_id]
        self.__depth = depth
        return None

    def add_origin(self, origin_id:int, origin_depth:int) -> None:
        self.__degree += 1
        self.__origins.append(origin_id)
        if (origin_depth + 1 < self.__depth):
            self.__depth = origin_depth + 1
        return None

    def get_degree(self) -> int:
        return self.__degree
    
    def get_name(self) -> str:
        return self.__name
    
    def get_origins(self) -> list[int]:
        return copy.deepcopy(self.__origins)

    def get_depth(self) -> int:
        return self.__depth

def main() -> int:
    print("Calling main function in requester")
    return 0

if __name__ == "__main__":
    main()