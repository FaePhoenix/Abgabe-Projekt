from graph.node import Node
from graph.edge import Edge
from cycles.cycle import Cycle

class Graph:
    def __init__(self, nodes:set[Node], edges:set[Edge]) -> None:
        self.__nodes:dict[int, Node] = { node.get_id() : node for node in nodes}
        self.__edges:dict[(int, int), Edge] = {(edge.get_start_id(), edge.get_end_id()) : edge for edge in edges}
        self.__extend_nodes()
        return None
    

    def get_origin(self) -> str:
        return self.__origin
    
    def calculate_cycles(self) -> set[Cycle]:
        return set()   

    def __extend_nodes(self) -> None:
        for edge in self.__edges.values():
            start_id = edge.get_start_id()
            end_id = edge.get_end_id()
            start = self.get_node_from_id(start_id)
            start.add_outgoing(edge)
            end = self.get_node_from_id(end_id)
            end.add_incoming(edge)

        return None
    
    def get_nodes(self) -> set[Node]:
        return set(self.__nodes.values())
    
    def get_edges(self) -> set[Edge]:
        return set(self.__edges.values())
    
    def get_density(self) -> float:
        node_count = len(self.__nodes)
        edge_count = len(self.__edges)
        return node_count / (edge_count * (edge_count - 1))
    
    def get_neighbours(self, node_id:int) -> list[Node]:
        outgoing_neighbour_ids = [edge.get_end_id() for edge in self.__edges.values() if edge.get_start_id() == node_id]
        incoming_neighbour_ids = [edge.get_start_id() for edge in self.__edges.values() if edge.get_end_id() == node_id]
        neighbour_ids = set(outgoing_neighbour_ids + incoming_neighbour_ids)

        return [self.__nodes.get(neighbour_id) for neighbour_id in neighbour_ids]
    
    def get_node_with_highest_in(self) -> Node:
        max_in = 0
        max_id = 0
        for node in self.__nodes.values():
            incoming = len(node.get_incoming())
            if incoming > max_in:
                max_in = incoming
                max_id = node.get_id()
        return self.__nodes.get(max_id)
    
    def get_node_with_highest_out(self) -> Node:
        max_out = 0
        max_id = 0
        for node in self.__nodes.values():
            outgoing = len(node.get_outgoing())
            if outgoing > max_out:
                max_out = outgoing
                max_id = node.get_id()
        return self.__nodes.get(max_id)
    
    def get_node_from_id(self, id:int) -> Node:
        return self.__nodes.get(id)

    
    def get_node_name(self, id:int) -> str | None:
        try:
            node = self.get_node_from_id(id)
        except Exception:
            return None
        return node.get_name()


def main() -> int:
    print("Calling main function in graph")
    return 0


if __name__ == "__main__":
    main()