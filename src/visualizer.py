import networkx as nx
import matplotlib.pyplot as plt
from filehelper import FileHelper


class Visualizer:
    def __init__(self) -> None:
        return None
    

def main() -> int:
    print("Calling main in visualizer")
    helper = FileHelper()
    graph = helper.read_graph_from_file(r"C:\Users\fae\Documents\Uni\Semester6\Skriptsprachen\Abgabe-Projekt\txtfiles\graph50.txt")
    G = nx.DiGraph()
    for node in graph.get_nodes():
        G.add_node(node.get_id())
    
    for edge in graph.get_edges():
        G.add_edge(edge.get_start_id(), edge.get_end_id())

    nx.draw_networkx(G, with_labels=True)
    plt.savefig(r"C:\Users\fae\Documents\Uni\Semester6\Skriptsprachen\Abgabe-Projekt\images\test50.png")
    return 0

if __name__ == "__main__":
    main()