from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from graph.graph import Graph
from graph.cycle import Cycle


class Edge:
    def __init__(self, start_id:int, end_id:int) -> None:
        self.__start_id:int = start_id
        self.__end_id:int = end_id
        self.__paths:list[list[int]] = [[self.__end_id]]
        return None
    
    def get_start_id(self) -> int:
        return self.__start_id
    
    def get_end_id(self) -> int:
        return self.__end_id
    
    def traverse(self, graph, cycles:set[Cycle]) -> bool:
        paths = self.__paths.copy()
        self.__paths = []
        for path in paths:
            last_id = path[-1]
            last_node = graph.get_node_from_id(last_id)
            for outgoing in last_node.get_outgoing():
                out_id = outgoing.get_end_id()            
                if out_id == path[0]:
                    cycles.add(Cycle(path))
                elif out_id not in path:
                    new_path = path.copy()
                    new_path.append(out_id)
                    self.__paths.append(new_path)
        return bool(self.__paths)


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

