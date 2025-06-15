from graph.node import Node
from graph.edge import Edge
from graph.cycle import Cycle
import time

class Graph:
    def __init__(self, nodes:set[Node], edges:set[Edge]) -> None:
        self.__nodes:dict[int, Node] = { node.get_id() : node for node in nodes}
        self.__edges:dict[(int, int), Edge] = {(edge.get_start_id(), edge.get_end_id()) : edge for edge in edges}
        self.__extend_nodes()
        return None
    
    def calculate_cycles(self) -> set[Cycle]:
        cycles = []
        changed = True
        changed_new = False
        while changed:
            changed_new = False
            start = time.time()
            nodes = self.__nodes.values()
            for node in nodes:
                node_start = time.time()
                changed_new = changed_new or node.traverse(self, cycles)
                print(f"Node took {time.time() - node_start}s")
            print(f"Step took {time.time() - start}s for {len(nodes)} nodes")
            changed = changed_new
        return cycles
        

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

    def get_all_direceted_cycles(self) -> set[Cycle]: #REDO w/ tarjan
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
        
        end_node = self.__nodes.get(path[-1])
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
    
    def get_node_name(self, id:int) -> str | None:
        try:
            node = self.__get_node_from_id(id)
        except Exception:
            return None
        return node.get_name()


def main() -> int:
    print("Calling main function in graph")
    return 0


if __name__ == "__main__":
    main()