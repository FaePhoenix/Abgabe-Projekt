from cycles.tarjan_node import TarjanNode

class TarjanGraph:
    def __init__(self, nodes:set[TarjanNode]) -> None:
        self.__nodes:dict[int, TarjanNode] = {node.get_id() : node for node in nodes}
        return None
    
    def get_nodes(self) -> set[TarjanNode]:
        return set(self.__nodes.values())
    
    def get_node_from_id(self, id:int) -> TarjanNode:
        return self.__nodes.get(id)
    

def main() -> int:
    print("Calling main in tarjan graph")
    return 0


if __name__ == "__main__":
    main()