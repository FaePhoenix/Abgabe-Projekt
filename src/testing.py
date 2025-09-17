from custom_io.filehelper import FileHelper
from logic.graphbuilder import GraphBuilder


def main() -> int:
    #Just used for testing out new components and how they work together with old components
    build_test()
    return 0

def build_test() ->None:
    builder = GraphBuilder(50, 10)
    graph = builder.build_graph_from_article("Linux", "n", True)

    assert graph

    helper = FileHelper()
    helper.write_graph_to_file(graph, f"{graph.get_root()}-test", True)
    return None

if __name__ == "__main__":
    main()