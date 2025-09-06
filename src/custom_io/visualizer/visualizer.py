from datastructures.graph.graph import Graph
import networkx as nx
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self) -> None:
        return None
    
    def save_image_from_graph(self, graph_ot_visualize:Graph, save_location:str, image_size:tuple[int, int], resolution:int, verbose:bool) -> None:
        drawable_graph = self.__convert_graph(graph_ot_visualize, verbose)

        fig = plt.figure(1, figsize=image_size, dpi=resolution)
        nx.draw_kamada_kawai(drawable_graph, with_labels=True, node_size=4_000, node_color="skyblue", linewidths=1, arrowsize=20, width=1, font_size=8, edge_color="lightgrey")
        
        if verbose:
            report_statement = '' \
            'Drawing done, saving to file'

            print(report_statement)        

        file_name = graph_ot_visualize.get_root() + "-" + str(len(graph_ot_visualize.get_nodes())) + ".png" 
        full_file_name = save_location + file_name
        plt.savefig(full_file_name)

        report_statement = '' \
        'Successfully saved image to file\n' \
        f'See {full_file_name}'

        print(report_statement)

        return None

    def __convert_graph(self, graph_ot_visualize:Graph, verbose:bool) -> nx.DiGraph:
        drawn_graph = nx.DiGraph()

        if verbose:
            report_statement = '' \
            'Converting graph object into drawable structure'

            print(report_statement)
        
        for node in graph_ot_visualize.get_nodes():
            drawn_graph.add_node(f"{node.get_name()}")

        if verbose:
            report_statement = '' \
            f'Successfully created {len(graph_ot_visualize.get_nodes())} nodes in converted graph'

            print(report_statement)

        for edge in graph_ot_visualize.get_edges():
            start_id = edge.get_start_id()
            start_name = graph_ot_visualize.get_node_name(start_id)

            end_id = edge.get_end_id()
            end_name = graph_ot_visualize.get_node_name(end_id)

            drawn_graph.add_edge(f"{start_name}", f"{end_name}")

        if verbose:
            report_statement = '' \
            f'Successfully created {len(graph_ot_visualize.get_edges())} edges in converted graph\n' \
            'Done converting graph, starting drawing'

            print(report_statement)

        return drawn_graph


def main() -> int:
    print("Calling main function in visualizer")
    return 0

if __name__ == "__main__":
    main()