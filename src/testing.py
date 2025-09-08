from custom_io.filehelper import FileHelper
from datastructures.cycles.tarjan_calculator import TarjanCalculator
import custom_io.visualizer.fancy_visualizer as vis
import os

def main() -> int:
    #Just used for testing out new components and how they work together with old components
    fancy_vis_test()
    return 0

def fancy_vis_test() -> None:
    vis.main()
    return None

def filepath_testing() -> None:
    disected = os.path.realpath(__file__).split('\\')
    project_path = "\\".join(disected[:len(disected) - 2])
    images = project_path + '\\images\\'
    txtfiles = project_path + '\\txtfiles\\'
    print(images + "\n" + txtfiles)
    return None

def cycle_testing() -> None:
    helper = FileHelper()
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