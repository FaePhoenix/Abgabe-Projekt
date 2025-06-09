from graphbuilder import GraphBuilder
from filehelper import FileHelper

def main() -> int:
    builder = GraphBuilder(max_graph_size = 20)
    built_graph = builder.build_graph_from_article("Licht")

    cycles = built_graph.get_all_direceted_cycles()
    for cycle in cycles:
        print(cycle)
    return 0


if __name__ == "__main__":
    main()