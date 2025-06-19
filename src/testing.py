from graphbuilder import GraphBuilder
from filehelper import FileHelper
from cycles.cycle_calculator import Cyclecalculator
from cycles.tarjan_calculator import TarjanCalculator

def main() -> int:
    #Just used for testing out new components and how they work together with old components
    helper = FileHelper()
    graph = helper.read_graph_from_file(r"C:\Users\fae\Documents\Uni\Semester6\Skriptsprachen\Abgabe-Projekt\txtfiles\graph500.txt")


    calc = TarjanCalculator()
    cycles = calc.find_strongly_connected_components(graph)

    for cycle in cycles:
        print(cycle)

    return 0


if __name__ == "__main__":
    main()