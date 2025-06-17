from cycles.cycle import Cycle
from graph.graph import Graph
from cycles.tarjan_graph import TarjanGraph
from cycles.tarjan_node import TarjanNode


class Cyclecalculator:
    def __init__(self) -> None:
        self.__stack:list[int]
        self.__index:int
        self.__sccs:list[list[int]]
        self.__graph:TarjanGraph
        return None
    
    def find_cycles(self, graph:Graph) -> set[Cycle]:
        tarjan_nodes = set()

        for node in graph.get_nodes():
            children = [edge.get_end_id() for edge in node.get_outgoing()]
            tarjan_node = TarjanNode(node.get_id(), children)
            tarjan_nodes.add(tarjan_node)

        tarjan_graph = TarjanGraph(tarjan_nodes)
        print("Successfully converted to Tarjan Graph")

        self.__calculate_sccs(tarjan_graph)

        print("Done finding scc's")
        cycles = set()

        for scc in self.__sccs:
            if len(scc) > 1:
                cycle = Cycle(scc)
                cycles.add(cycle)

        print("Converted scc's to cycles")

        return cycles

    
    def __calculate_sccs(self, graph:TarjanGraph) -> None:
        self.__graph = graph
        self.__index = 0
        self.__stack = []
        self.__sccs = []

        for node in graph.get_nodes():
            if node.get_index() == -1:
                print(f"Start calling strong connect on node {node.get_id()}")
                self.__strong_connect(node)
            else:
                print(f"Found {node} to have index {node.get_index()} other than -1")
        return None
    
    def __strong_connect(self, node:TarjanNode) -> None:
        print(f"Calling strong connect on node {node.get_id()}")
        node.set_index(self.__index)
        node.set_lowlink(self.__index)
        self.__index += 1

        self.__stack.append(node.get_id())
        print(f"Putting {node.get_id()} on the stack")

        for child_id in node.get_children():
            child = self.__graph.get_node_from_id(child_id)
            if child.get_index() == -1:
                print(f"Node {node.get_id()} encountered child {child_id} which is unkown")
                self.__strong_connect(child)
                node.set_lowlink(min(node.get_lowlink(), child.get_lowlink()))

            elif child_id in self.__stack:
                print(f"Node {node.get_id()} encountered child {child_id} which is already seen")
                node.set_index(min(node.get_lowlink(), child.get_index()))

        if node.get_lowlink() == node.get_index():
            self.__build_scc_from_stack(node.get_id())
        return None
    
    def __build_scc_from_stack(self, scc_start:int) -> None:
        print("Found scc")
        scc = []
        while len(self.__stack) > 0:
            node_id = self.__stack.pop(-1)
            scc.append(node_id)
            if node_id == scc_start:
                break
                
        self.__sccs.append(scc)
        print(f"Removing {scc} from the stack")  
        return None
      

def main() -> int:
    print("Calling main in cycle calculator")
    return 0


if __name__ == "__main__":
    main()