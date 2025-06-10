from graphbuilder import GraphBuilder
from filehelper import FileHelper

def main() -> int:

    helper = FileHelper()
    built_graph = helper.read_graph_from_file(r"C:\Users\fae\Documents\Uni\Semester6\Skriptsprachen\Abgabe-Projekt\txtfiles\graph50.txt")
    #builder = GraphBuilder(max_graph_size = 50)

    #built_graph = builder.build_graph_from_article("Licht")

    #helper.write_graph_to_file(built_graph, r"C:\Users\fae\Documents\Uni\Semester6\Skriptsprachen\Abgabe-Projekt\txtfiles\graph50.txt")

    cycles = built_graph.calculate_cycles()
    for cycle in set(cycles):
        print(cycle)
    return 0


if __name__ == "__main__":
    main()