from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graph.graph import Graph
    from graph.edge import Edge
from graph.cycle import Cycle

class Node:
    def __init__(self, id:int, name:str, keywords:list[str], depth:int) -> None:
        self.__id:int = id
        self.__name:str = name
        self.__keywords:list[str] = keywords
        self.__depth:int = depth
        self.__in:dict[(int, int), Edge] = {}
        self.__out:dict[(int, int), Edge] = {}
        return None

    def __hash__(self) -> int:
        self_content = (self.__id, self.__name, tuple(self.__keywords), self.__depth)
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
    
    def get_incoming(self) -> list[Edge]:
        return list(self.__in.values())
    
    def add_incoming(self, incoming:Edge) -> None:
        self.__in[(incoming.get_start_id(), incoming.get_end_id())] = incoming
        return None
    
    def get_outgoing(self) -> list[Edge]:
        return list(self.__out.values())
    
    def add_outgoing(self, outgoing:Edge) -> None:
        self.__out[(outgoing.get_start_id(), outgoing.get_end_id())] = outgoing
        return None


def main() -> int:
    print("Calling main function in node")
    return 0


if __name__ == "__main__":
    main()