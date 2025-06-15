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
    graph = helper.read_graph_from_file(r"C:\Users\fae\Documents\Uni\Semester6\Skriptsprachen\Abgabe-Projekt\txtfiles\graph500.txt")

    drawn_graph = nx.DiGraph()

    node_count = len(graph.get_nodes())
    finished_nodes = 0
    for node in graph.get_nodes():
        drawn_graph.add_node(f"{node.get_name()}")
        finished_nodes += 1
        print(f"Node drawing: {(100*finished_nodes/node_count):.2f}%")
        #drawn_graph.add_node(f"({node.get_name()}, {node.get_id()})")

    finished_edges = 0
    edge_count = len(graph.get_edges())
    for edge in graph.get_edges():
        start_id = edge.get_start_id()
        start_name = graph.get_node_name(start_id)

        end_id = edge.get_end_id()
        end_name = graph.get_node_name(end_id)

        #drawn_graph.add_edge(f"({start_name}, {start_id})", f"({end_name}, {end_id})")
        drawn_graph.add_edge(f"{start_name}", f"{end_name}")
        finished_edges += 1
        if finished_edges % 50 == 0:
            print(f"Edges drawing: {(100*finished_edges/edge_count):.2f}%")

    fig = plt.figure(1, figsize=(150, 90), dpi=100)
    print("Finished plt figure")

    nx.draw_kamada_kawai(drawn_graph, with_labels=True, node_size=4_000, node_color="skyblue", linewidths=1, arrowsize=20, width=1, font_size=8, edge_color="lightgrey")
    print("Finished networkx graph")

    plt.savefig(r"C:\Users\fae\Documents\Uni\Semester6\Skriptsprachen\Abgabe-Projekt\images\graph500.png")
    print("Done")
    return 0

if __name__ == "__main__":
    main()