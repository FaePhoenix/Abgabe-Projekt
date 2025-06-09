from graph.node import Node
from graph.edge import Edge
from graph.cycle import Cycle

class Graph:
    def __init__(self, nodes:set[Node], edges:set[Edge]) -> None:
        self.__nodes = nodes
        self.__edges = edges
        self.__extend_nodes()
        return None
    
    def __extend_nodes(self) -> None:
        for edge in self.__edges:
            start_id = edge.get_start_id()
            end_id = edge.get_end_id()
            start = self.__get_node_from_id(id = start_id)
            start.add_outgoin(id = end_id)
            end = self.__get_node_from_id(id = end_id)
            end.add_incoming(id = start_id)

        return None
    
    def get_nodes(self) -> set[Node]:
        return self.__nodes
    
    def get_edges(self) -> set[Edge]:
        return self.__edges
    
    def get_density(self) -> float:
        node_count = len(self.__nodes)
        edge_count = len(self.__edges)
        return node_count / (edge_count * (edge_count - 1))
    
    def get_neighbours(self, node_id:int) -> list[Node]:
        outgoing_neighbour_ids = [edge.get_end_id() for edge in self.__edges if edge.get_start_id() == node_id]
        incoming_neighbour_ids = [edge.get_start_id() for edge in self.__edges if edge.get_end_id() == node_id]
        neighbour_ids = set(outgoing_neighbour_ids + incoming_neighbour_ids)

        return [self.__get_node_from_id(id = neighbour_id) for neighbour_id in neighbour_ids]
    
    def get_node_with_highest_in(self) -> Node:
        max_in = 0
        max_id = 0
        for node in self.__nodes:
            incoming = node.get_incoming()
            if incoming > max_in:
                max_in = incoming
                max_id = node.get_id()
        return self.__get_node_from_id(id = max_id)
    
    def get_node_with_highest_out(self) -> Node:
        max_out = 0
        max_id = 0
        for node in self.__nodes:
            outgoing = node.get_outgoing()
            if outgoing > max_out:
                max_out = outgoing
                max_id = node.get_id()
        return self.__get_node_from_id(id = max_id)
    
    def __get_node_from_id(self, id:int) -> Node:
        for node in self.__nodes:
            if node.get_id() == id:
                return node


    def get_all_direceted_cycles(self) -> set[Cycle]:
        cycles = set()
        start_nodes = [node.get_id() for node in self.__nodes]

        while len(start_nodes) != 0:
            next_node = start_nodes.pop(0)
            print(f"Starting run w/ {next_node}")

            new_cycles = self.__directed_cycle_finder(path = [next_node])
            cycles.update(new_cycles)

            found_nodes = set()
            for cycle in new_cycles:
                found_nodes.update(cycle.get_path())
            
            removable = set(start_nodes) & found_nodes
            for id in removable:
                start_nodes.remove(id)

        return cycles
    
    def __directed_cycle_finder(self, path:list[int]) -> set[Cycle]:
        if path[-1] in path[:-1]:

            found_cycle = Cycle(path[path.index(path[-1]):-1])
            print(f"Found cycle \"{found_cycle}\" in: {path}")
            return set([found_cycle])
        
        end_node = self.__get_node_from_id(path[-1])
        next_nodes = end_node.get_outgoing()

        found_cycles = set()

        if len(next_nodes) == 0:
            print(f"Found dead end for {path}")
            return found_cycles
        
        for node in next_nodes:
            new_path = path.copy()
            new_path.append(node)
            found_cycles.update(self.__directed_cycle_finder(path = new_path))

        return found_cycles


def main() -> int:
    print("Calling main function in graph")
    return 0


if __name__ == "__main__":
    main()