from logic.graphbuilder import GraphBuilder
from custom_io.filehelper import FileHelper
from datastructures.graph.graph import Graph
import networkx as nx
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, ) -> None:
        return None
    
    def save_image_from_graph(self, graph_ot_visualize:Graph, save_location:str, image_size:tuple[int, int] = (150, 90), resolution:int = 100, labled:bool = True) -> None:
        drawn_graph = nx.DiGraph()

        for node in graph_ot_visualize.get_nodes():
            drawn_graph.add_node(f"{node.get_name()}")

        for edge in graph_ot_visualize.get_edges():
            start_id = edge.get_start_id()
            start_name = graph_ot_visualize.get_node_name(start_id)

            end_id = edge.get_end_id()
            end_name = graph_ot_visualize.get_node_name(end_id)

            drawn_graph.add_edge(f"{start_name}", f"{end_name}")

        fig = plt.figure(1, figsize=image_size, dpi=resolution)
        nx.draw_kamada_kawai(drawn_graph, with_labels=labled, node_size=4_000, node_color="skyblue", linewidths=1, arrowsize=20, width=1, font_size=8, edge_color="lightgrey")
        
        filename = graph_ot_visualize.get_root() + "_" + str(len(graph_ot_visualize.get_nodes())) + ".png"
        plt.savefig(save_location + filename)

        return None
    

    

def main() -> int:
    print("Calling main function in visualizer")
    return 0

if __name__ == "__main__":
    main()