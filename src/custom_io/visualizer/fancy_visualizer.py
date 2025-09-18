import pyvis.network as pynet
from datastructures.graph.graph import Graph
from datastructures.cycles.cycle import Cycle

class FancyVisualizer:
    def __init__(self, settings:dict[str, str]) -> None:
        self.__settings = settings
        return None
    
    def generate_browser_graph(self, graph:Graph, verbose:bool) -> None:

        custom_height = self.__settings.get("height")
        assert custom_height

        custom_width = self.__settings.get("width")
        assert custom_width

        custom_bgcolor = self.__settings.get("bgcolor")
        assert custom_bgcolor

        custom_node_color = self.__settings.get("nodecolor")
        assert custom_node_color

        if verbose:
            report_statement = '' \
            'Settings selected' \
            f'heigth, width: {custom_height}, {custom_width}' \
            f'background color: {custom_bgcolor}' \
            f'node color: {custom_node_color}' \
            ' Starting with building of interactive visualization'

            print(report_statement)

        network = pynet.Network(height = custom_height, width = custom_width, bgcolor = custom_bgcolor, directed = True)


        nodes = list(graph.get_nodes())
        for node in nodes:
            network.add_node(n_id=node.get_id(), label = node.get_name(), color = custom_node_color)

        if verbose:
            report_statement = '' \
            f'Successfully added {len(nodes)} nodes to the interactive graph.\n' \
            'Loading edges'

            print(report_statement)

        edges = list(graph.get_edges())
        for edge in edges:
            network.add_edge(source = edge.get_start_id(), to = edge.get_end_id())

        if verbose:
            report_statement = '' \
            f'Successfully added {len(edges)} edges to the interactive graph.\n' \
            'Starting spring-based physics simulation'

            print(report_statement)

        network.barnes_hut()

        graph_name = f"{graph.get_root()}-{len(nodes)}.html"

        if verbose:
            report_statement = '' \
            'Successfully built interactive graph.\n' \
            'Browser should open and the result will be saved in the project folder with the name:\n'\
            f'{graph_name}'

            print(report_statement)
        
        network.show(name = graph_name)
        return None
    
    def generate_cycle_graph(self, cyclic_graph:Graph, id:int) -> None:

        custom_height = self.__settings.get("height")
        assert custom_height

        custom_width = self.__settings.get("width")
        assert custom_width

        custom_bgcolor = self.__settings.get("bgcolor")
        assert custom_bgcolor

        custom_node_color = self.__settings.get("nodecolor")
        assert custom_node_color

        network = pynet.Network(height = custom_height, width = custom_width, bgcolor = custom_bgcolor, directed = True)

        nodes = list(cyclic_graph.get_nodes())
        for node in nodes:
            network.add_node(n_id=node.get_id(), label = node.get_name(), color = custom_node_color)

        edges = list(cyclic_graph.get_edges())
        for edge in edges:
            network.add_edge(source = edge.get_start_id(), to = edge.get_end_id())

        network.barnes_hut()

        file_name = f"{cyclic_graph}-{id}.html"
        network.show(file_name)

        return None
def main() -> int:
    print("Calling main function in visualizer")
    return 0


if __name__ == "__main__":
    main()