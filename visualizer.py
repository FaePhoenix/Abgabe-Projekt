import pyvis.network as pynet
from graphbuilder import GraphBuilder


class Visualizer:
    def __init__(self) -> None:
        return None
    

def main() -> int:
    print("Calling main function in visualizer")
    builder = GraphBuilder(max_graph_size = 20  , max_depth = 10)
    graph = builder.build_graph_from_article(start_name = "Licht")
    print(f"graph done")

    net = pynet.Network(height = "1500px", width = "100%", directed = True, bgcolor = "#00052E", font_color = "white")
    
    nodes = list(graph.get_nodes())
    for node in nodes:
        net.add_node(n_id = node.get_id(), label = node.get_name())

    edges = list(graph.get_edges())
    for edge in edges:
        net.add_edge(source = edge.get_start_id(), to = edge.get_end_id())

    net.barnes_hut()
    net.show(name = "output.html", notebook = False)

    return 0


if __name__ == "__main__":
    main()