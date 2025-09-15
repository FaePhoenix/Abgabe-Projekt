from datastructures.graph.graph import Graph
from datastructures.graph.node import Node
from datastructures.cycles.tarjan_graph import TarjanGraph
from datastructures.cycles.tarjan_node import TarjanNode
from datastructures.cycles.tarjan_calculator import TarjanCalculator
from datastructures.cycles.cycle import Cycle


class CircleManager:
    def __init__(self) -> None:
        self.__partitions:set[Graph]
        return None
    
    def get_directed_cycles(self, graph:Graph, verbose:bool, max_cycle_size:int|None) -> set[Cycle]:

        converted_graph = self.__generate_tarjan_graph(graph, verbose)

        tarjan_calc = TarjanCalculator()
        sccs = tarjan_calc.calculate_sccs(converted_graph, verbose)

        self.__partitions = self.__convert_sccs(sccs, graph, verbose)

        if not max_cycle_size:
            max_cycle_size = len(graph.get_nodes())

        cycles = self.__get_cycles_from_partitions(max_cycle_size, verbose)

        filtered_cycles = self.__filter_cycles(cycles, verbose)

        return filtered_cycles
    
    def get_undirected_cycles(self, graph:Graph, verbose:bool, max_cycle_size:int|None) -> set[Cycle]:

        if not max_cycle_size:
            max_cycle_size = len(graph.get_nodes())

        cycles = self.__get_nondirectional_cycles(graph, max_cycle_size, verbose)

        filtered_cycles = self.__filter_cycles(cycles, verbose)

        return filtered_cycles
    
    def __get_nondirectional_cycles(self, graph:Graph, max_depth:int, verbose:bool) -> set[Cycle]:
        nodes = graph.get_nodes()

        all_cycles = set()

        for count, node in enumerate(nodes):
            new_cycles = self.__get_nondirectional_cycles_from_graph(graph, node, max_depth)
            all_cycles.update(new_cycles)

            if verbose:
                report_statement = '' \
                f'Found {len(new_cycles)} new cycles before filtering out duplicates.\n' \
                f'{(count/len(nodes) * 100):.2f}% done'
        
                print(report_statement)

        return all_cycles
    
    def __get_nondirectional_cycles_from_graph(self, graph:Graph, next_node:Node, max_depth:int, path:list[int]|None = None) -> set[Cycle]:
        if not path:
            path = []

        next_node_id = next_node.get_id()

        if next_node_id in path:
            circle_start = path.index(next_node_id)
            cut_path = path[circle_start:]
            found_cycle = Cycle(cut_path)

            return {found_cycle}
        
        if len(path) +1 == max_depth:
            return set()
        
        path.append(next_node_id)

        out_going_edges = next_node.get_outgoing()
        out_child_ids = [edge.get_end_id() for edge in out_going_edges]

        in_going_edges = next_node.get_incoming()
        in_child_ids = [edge.get_start_id() for edge in in_going_edges]

        children_ids = out_child_ids + in_child_ids
        children = [graph.get_node_from_id(id) for id in children_ids]
        filtered_children = [child for child in children if child]
        
        cycles = set()

        for child in filtered_children:
            child_cycles = self.__get_nondirectional_cycles_from_graph(graph, child, max_depth, path)
            cycles.update(child_cycles)

            
        return cycles
    
    def __generate_tarjan_graph(self, graph:Graph, verbose:bool) -> TarjanGraph:
        tarjan_nodes = set()

        nodes = graph.get_nodes()
        
        counter = 0
        if verbose:
           
            report_statement = '' \
            f'Converting {len(nodes)} nodes'

            print(report_statement)

        for node in nodes:
            children = [edge.get_end_id() for edge in node.get_outgoing()]
            tarjan_node = TarjanNode(node.get_id(), children)
            tarjan_nodes.add(tarjan_node)
            counter += 1
            if verbose:
                report_statement = '' \
                f'{(counter/len(nodes) * 100):.2f}%'

                print(report_statement)

        if verbose:
            report_statement = '' \
            'Conversion done'

            print(report_statement)

        return TarjanGraph(tarjan_nodes)
    
    def __convert_sccs(self, sccs:list[list[int]], graph:Graph, verbose:bool) -> set[Graph]:
        partitions = set()
        
        if verbose:
            report_statement = '' \
            f'Converting {len(sccs)} components into graphs'

            print(report_statement)

        for scc in sccs:

            if len(scc) < 3:
                if verbose:
                    report_statement = '' \
                    'Found component of only 2 nodes.\n' \
                    'Skipping'

                    print(report_statement)

                continue
            
            if verbose:
                report_statement = '' \
                f'Converting component of size {len(scc)}'

                print(report_statement)

            partial_graph = self.__build_partial_graph(graph, verbose, scc)    

            partitions.add(partial_graph)

        return partitions

    def __build_partial_graph(self, graph:Graph, verbose:bool, scc:list[int]) -> Graph:
        nodes:set[Node] = set()

        for id in scc:
            original_node = graph.get_node_from_id(id)
            assert original_node
            nodes.add(original_node)

        if verbose:
            report_statement = '' \
                'Nodes created.\n' \
                'Building edges'

            print(report_statement)

        edges = set()
        for node in nodes:
            filtered_out_going = [edge for edge in node.get_outgoing() if edge.get_end_id() in scc]

            for edge in filtered_out_going:
                edges.add(edge)

        if verbose:
            report_statement = '' \
                f'Created {len(edges)} edges'

            print(report_statement)

        root_id = scc[0]
        root = graph.get_node_from_id(root_id)            

        assert root

        root_name = root.get_name()

        if verbose:
            report_statement = '' \
                f'Picked {root_name} ({root_id}) as root for partial graph'

            print(report_statement)

        partial_graph = Graph(root_name, nodes, edges)

        return partial_graph
    
    def __get_cycles_from_partitions(self, max_depth:int, verbose:bool) -> set[Cycle]:
        cycles = set()

        for graph in self.__partitions:
            random_node = list(graph.get_nodes())[0]

            if verbose:
                report_statement = '' \
                f'Using {random_node.get_name()} ({random_node.get_id()}) as starting point for partial graph of size {len(graph.get_nodes())}'

                print(report_statement)

            partial_cycles = self.__get_cycles_from_partition(graph, random_node, max_depth)
            cycles.update(partial_cycles)

            if verbose:
                report_statement = '' \
                f'Found {len(partial_cycles)}'

                print(report_statement)

        if verbose:
            report_statement = '' \
            f'Done and found {len(cycles)} cycles'

            print(report_statement)

        return cycles

    def __get_cycles_from_partition(self, graph:Graph, next_node:Node, max_depth:int, path:list[int]|None = None) -> set[Cycle]:
        if not path:
            path = []
        
        next_node_id = next_node.get_id()

        if next_node_id in path:
            circle_start = path.index(next_node_id)
            cut_path = path[circle_start:]
            found_cycle = Cycle(cut_path)

            return {found_cycle}
        
        if len(path) + 1 == max_depth:
            return set()
        
        path.append(next_node_id)
        
        out_going_edges = next_node.get_outgoing()
        child_ids = [edge.get_end_id() for edge in out_going_edges]
        children = [graph.get_node_from_id(id) for id in child_ids]
        filtered_children = [child for child in children if child]

        cycles = set()

        for child in filtered_children:
            child_cycles = self.__get_cycles_from_partition(graph, child, max_depth, path)
            cycles.update(child_cycles)

        return cycles

    def __filter_cycles(self, cycles:set[Cycle], verbose:bool) -> set[Cycle]:

        filtered_cycles = set([cycle for cycle in cycles if len(cycle.get_path()) > 2])

        if verbose:
            report_statement = '' \
            f'From {len(cycles)} found cycles, {len(filtered_cycles)} are true cycles.\n' \
            'Discarding the rest'

            print(report_statement)

        return filtered_cycles