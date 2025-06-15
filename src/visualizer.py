from graphbuilder import GraphBuilder
from filehelper import FileHelper
import networkx as nx
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self) -> None:
        return None
    

def main() -> int:
    print("Calling main function in visualizer")

    helper = FileHelper()
    graph = helper.read_graph_from_file(r"C:\Users\fae\Documents\Uni\Semester6\Skriptsprachen\Abgabe-Projekt\txtfiles\graph50.txt")

    drawn_graph = nx.DiGraph()

    for node in graph.get_nodes():
        drawn_graph.add_node(f"{node.get_name()}")
        #drawn_graph.add_node(f"({node.get_name()}, {node.get_id()})")

    for edge in graph.get_edges():
        start_id = edge.get_start_id()
        start_name = graph.get_node_name(start_id)

        end_id = edge.get_end_id()
        end_name = graph.get_node_name(end_id)

        #drawn_graph.add_edge(f"({start_name}, {start_id})", f"({end_name}, {end_id})")
        drawn_graph.add_edge(f"{start_name}", f"{end_name}")

    fig = plt.figure(1, figsize=(35, 25), dpi=120)
    nx.draw_kamada_kawai(drawn_graph, with_labels=True, node_size=4_000, node_color="skyblue", linewidths=1, arrowsize=20, width=1, font_size=8, edge_color="lightgrey")
    plt.savefig(r"C:\Users\fae\Documents\Uni\Semester6\Skriptsprachen\Abgabe-Projekt\images\graph50.png")
    return 0

if __name__ == "__main__":
    main()