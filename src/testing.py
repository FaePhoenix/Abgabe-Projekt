from graphbuilder import GraphBuilder
from filehelper import FileHelper
from cycles.cycle_calculator import Cyclecalculator

def main() -> int:
    helper = FileHelper()
    graph = helper.read_graph_from_file(r"C:\Users\fae\Documents\Uni\Semester6\Skriptsprachen\Abgabe-Projekt\txtfiles\graph.txt")


    calc = Cyclecalculator()
    cycles = calc.find_cycles(graph)

    for cycle in cycles:
        print(cycle)

    return 0


if __name__ == "__main__":
    main()