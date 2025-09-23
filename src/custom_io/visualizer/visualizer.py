from datastructures.graph.graph import Graph

import networkx as nx
import matplotlib.pyplot as plt


class Visualizer:
    """
    A class organizing the creation of image files from graphs

    Methods:
    --------
    save_image_from_graph(graph : Graph, save_location : str, image_size : tuple[int, int], resolution : int, verbose : bool) -> None
        Create an image from a graph and save it to a file
    """

    def __init__(self) -> None:
        """
        Sets up the object
        """
        return None
    
    def save_image_from_graph(self, graph:Graph, save_location:str, image_size:tuple[int, int], resolution:int, verbose:bool) -> None:
        """
        Creating an image from a graph and save it to a file

        Parameters:
        -----------
        graph : Graph
            Graph to create an image of

        save_location : str
            Folder location in which to save the image file

        image_size : tuple[int, int]
            The size of the image in width and heigth

        resolution : int
            The resolution of the image

        verbose : bool
            Should the action be logged verbosely
        """

        drawable_graph = self.__convert_graph(graph, verbose)

        fig = plt.figure(f"{graph.get_root()}-{len(graph.get_nodes())}", figsize=image_size, dpi=resolution)
        nx.draw_kamada_kawai(drawable_graph, with_labels=True, node_size=4_000, node_color="skyblue", linewidths=1, arrowsize=20, width=1, font_size=8, edge_color="lightgrey")
        
        if verbose:
            report_statement = '' \
            'Drawing done, saving to file'

            print(report_statement)        

        file_name = graph.get_root() + "-" + str(len(graph.get_nodes())) + ".png" 
        full_file_name = save_location + file_name
        plt.savefig(full_file_name)

        report_statement = '' \
        'Successfully saved image to file\n' \
        f'See {full_file_name}'

        print(report_statement)

        return None

    def __convert_graph(self, graph:Graph, verbose:bool) -> nx.DiGraph:
        """
        Converts the given graph into a graph from the networkx module

        Parameters:
        -----------
        graph : Graph
            The graph to convert

        verbose : bool
            Should the action be logged verbosely
        """
        drawn_graph = nx.DiGraph()

        if verbose:
            report_statement = '' \
            'Converting graph object into drawable structure'

            print(report_statement)
        
        for node in graph.get_nodes():
            drawn_graph.add_node(f"{node.get_name()}")

        if verbose:
            report_statement = '' \
            f'Successfully created {len(graph.get_nodes())} nodes in converted graph'

            print(report_statement)

        for edge in graph.get_edges():
            start_id = edge.get_start_id()
            start_name = graph.get_node_name(start_id)

            end_id = edge.get_end_id()
            end_name = graph.get_node_name(end_id)

            drawn_graph.add_edge(f"{start_name}", f"{end_name}")

        if verbose:
            report_statement = '' \
            f'Successfully created {len(graph.get_edges())} edges in converted graph\n' \
            'Done converting graph, starting drawing'

            print(report_statement)

        return drawn_graph


def main() -> int:
    print("Calling main function in visualizer")
    return 0

if __name__ == "__main__":
    main()