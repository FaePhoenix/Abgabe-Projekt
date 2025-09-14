from custom_io.filehelper import FileHelper
from datastructures.cycles.circle_manager import CircleManager
import custom_io.visualizer.fancy_visualizer as vis
import os



def main() -> int:
    #Just used for testing out new components and how they work together with old components
    cycle_testing()
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
    graphfile = "Linux-2000.txt"
    graph = helper.read_graph_from_file(graphfile, False)

    if not graph:
        print("Failed to read graph")
        return None

    calc = CircleManager()
    cycles = calc.get_directed_cycles(graph, True, 1000)

    for cycle in cycles:
        print(cycle)

    return None

if __name__ == "__main__":
    main()