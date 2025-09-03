from logic.fetch.sorter import Sorter
from custom_io.filehelper import FileHelper
from datastructures.cycles.tarjan_calculator import TarjanCalculator


def main() -> int:
    #Just used for testing out new components and how they work together with old components
    sorter_types_testing()
    return 0

def sorter_types_testing() -> None:
    sorter = Sorter()
    sorter.get_content("Licht")
    return None

def py_testing() -> None:
    links = ["a", "b", "c", "d"]
    entries = ["a", "e", "d"]

    if (name := entries[0]) in links:
        print(f"Found {name}")

    return None

def cycle_testing() -> None:
    helper = FileHelper("")
    graphfile = r"C:\Users\fae\Documents\Uni\Semester6\Skriptsprachen\Abgabe-Projekt\txtfiles\graph500.txt"
    graph = helper.read_graph_from_file(graphfile, False)

    if not graph:
        print("Failed to read graph")
        return None

    calc = TarjanCalculator()
    cycles = calc.find_strongly_connected_components(graph)

    for cycle in cycles:
        print(cycle)

    return None

if __name__ == "__main__":
    main()