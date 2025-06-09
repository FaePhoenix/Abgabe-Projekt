from __future__ import annotations


class Node:
    def __init__(self, id:int, name:str, keywords:list[str], depth:int) -> None:
        self.__id:int = id
        self.__name:str = name
        self.__keywords:list[str] = keywords
        self.__depth:int = depth
        self.__in:list[int] = []
        self.__out:list[int] = []
        return None

    def __hash__(self) -> int:
        self_content = (self.__id, self.__name, self.__keywords, self.__depth)
        return hash(self_content)
    
    def __eq__(self, other) -> bool:
        if other == None or not isinstance(other, Node):
            return False
        return self.__id == other.__id
        
    def __repr__(self) -> str:
        return f"(id:{self.__id}| name:{self.__name}| depth:{self.__depth}| keywords:{",".join(self.__keywords)})"
    
    def get_name(self) -> str:
        return self.__name
    
    def get_id(self) -> int:
        return self.__id
    
    def get_depth(self) -> int:
        return self.__depth
    
    def get_keywords(self) -> list[str]:
        return self.__keywords
    
    def get_incoming(self) -> list[int]:
        return self.__in
    
    def add_incoming(self, id:int) -> None:
        self.__in.append(id)
        return None
    
    def get_outgoing(self) -> list[int]:
        return self.__out
    
    def add_outgoin(self, id:int) -> None:
        self.__out.append(id)
        return None


def main() -> int:
    print("Calling main function in node")
    return 0


if __name__ == "__main__":
    main()