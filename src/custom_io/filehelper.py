from datastructures.cycles.cycle import Cycle
from datastructures.graph.graph import Graph
from datastructures.graph.node import Node
from datastructures.graph.edge import Edge

import os




class FileHelper:
    """
    A class encapsulating methods for handeling graph files

    Methods:
    --------
    write_graph_to_file(graph : Graph, file_name : str)
        Writes the given graph into a file at filename

    read_graph_from_file(file_name : str)
        Reads the file at file_name and returns the saved graph
    """

    def __init__(self) -> None:
        """
        Sets up the object
        """
        disected_file_position = os.path.realpath(__file__).split("\\")
        project_folder = "\\".join(disected_file_position[:len(disected_file_position) - 3])
        self.__directory = project_folder + "\\"
        self.__setup_folders()
        return None
    
    def write_cycles_to_file(self, origin_graph:Graph, cycles:list[Cycle]) -> None:

        cycle_lines = []
        for idx, cycle in enumerate(cycles):
            cycle_line = u""
            
            cycle_line += str(idx) + "\t"

            path = cycle.get_path()

            named_path = [origin_graph.get_node_name(id) for id in path]
            filtered_named_path = [name for name in named_path if name]

            cycle_in_text = " -> ".join(filtered_named_path)

            cycle_line += cycle_in_text
            
            cycle_lines.append(cycle_line)

        to_write = "\n".join(cycle_lines)

        file_name = f"{origin_graph.get_root()}-{len(origin_graph.get_nodes())}-cycles.txt"

        self.__write_to_file(file_name, to_write)

        return None
    
    def write_graph_to_file(self, graph:Graph, file_name:str, verbose:bool) -> None:
        """
        Writes the given graph into a file with the name file_name in a text format

        Parameters:
        -----------
        graph : Graph
            The graph to save

        file_name : str
            The location to save to
        
        verbose : bool
            Should the action be logged verbosely
        """

        to_write = u""
        nodes = list(graph.get_nodes())
        node_count = len(nodes)
        root = graph.get_root()
        to_write += f"{node_count};{root}\n"
        
        nodes.sort(key = lambda node : node.get_id())

        if verbose:
            print(f"Sorted {node_count} nodes by id for edge-matrix")

        for node in nodes:
            to_write += f"{node.get_id()};{node.get_name()};{node.get_depth()};{u",".join(node.get_keywords())}\n"

        if verbose:
            print("Successfully generated node-text")

        connection_matrix = [[-1 for _ in range(node_count)] for _ in range(node_count)]
        
        ids = [node.get_id() for node in nodes]

        for row_idx, start_id in enumerate(ids):
            start_node = graph.get_node_from_id(start_id)
            assert start_node
            out_ids = [edge.get_end_id() for edge in start_node.get_outgoing()]
            for col_idx, end_id in enumerate(ids):
                if end_id in out_ids:
                    connection_matrix[row_idx][col_idx] = 1
                else:
                    connection_matrix[row_idx][col_idx] = 0
        
        if verbose:
            print("Successfully generated connection matrix")

        for row in connection_matrix:
            to_write += f"{" ".join(map(str, row))}\n"
        
        if verbose:
            print("Successfully converted connection matrix into edge-text")

        to_write = to_write.rstrip("\n")

        if verbose:
            print("Successfully generated graph-text")

        self.__write_to_file(file_name, to_write)

        return None
    
    def __write_to_file(self, file_name:str, file_content:str) -> None:
        full_file_name = self.__directory + "txtfiles\\" + file_name

        writing_parameter = "x"

        while os.path.exists(full_file_name):
            warning_statement = '' \
            f'File \"{file_name}\" already exists in the txtfiles-folder.\n' \
            'Please specify if you want to (o) overwrite the existing file, (r) to rename the new file or (s) to skip saving graph.\n'

            user_repsonse = input(warning_statement)

            match user_repsonse:
                case "o":
                    writing_parameter = "w"
                    break
                
                case "r":
                    report_statement = '' \
                    'Please give a new file_name:'

                    file_name = input(report_statement)
                    full_file_name = self.__directory + "txtfiles\\" + file_name

                case "s":
                    report_statement = '' \
                    'Skipping saving of graph'

                    print(report_statement)

                    return None

                case _:
                    warning_statement = '' \
                    f'Given response \"{user_repsonse}\" was neither o to override nor r to rename\n' \
                    'Please try again'

                    print(warning_statement)

        with open(file = full_file_name, mode = writing_parameter, encoding="UTF8") as file:
            file.write(file_content)

        return None
    
    def read_graph_from_file(self, file_name:str, verbose:bool) -> Graph | None:
        """
        Reads the file named file_name in the current directory and returns the saved graph

        Parameters:
        -----------
        file_name : str
            The location to read
        verbose : bool
            Should the action be logged verbosely
        """

        full_file_name = self.__directory + 'txtfiles\\' + file_name
        file_content = self.__read_file(full_file_name)
        
        if file_content == None:
            failure_statement = '' \
            f'Given file: {full_file_name} is empty\n' \
            'Abort graph reading'
            
            print(failure_statement)
            return None
        
        if verbose:
            print(f"Reading file: {full_file_name}\nFound {len(file_content)} lines")

        first_line = file_content[0]
        count, root = first_line.rstrip("\n").split(";")
        node_count = int(count)
        node_lines = file_content[1:node_count + 1]

        if verbose:
            print(f"Expecting {node_count} nodes for root: {root}")

        nodes = set(self.__extract_nodes(node_lines))
        node_ids = [node.get_id() for node in nodes]

        if verbose:
            print(f"Successfully read {len(node_ids)} Nodes")

        edge_lines = file_content[node_count + 1:len(file_content)]
        edges = self.__extract_edges(edge_lines, node_ids)
        
        if verbose:
            print(f"Successfully read {len(edges)} Edges")

        return Graph(root, nodes, edges)

    def __extract_nodes(self, node_lines:list[str]) -> list[Node]:
        """
        Converts the saved text format into a list of Node objects

        Paramters:
        ----------
        node_lines : list[str]
            The lines of the saved graph file that contain node information
        """

        nodes = []
        for line in node_lines:
            node_attributes = line.split(";")
            node_id = int(node_attributes[0])
            name = node_attributes[1]
            depth = int(node_attributes[2])
            cleaned = node_attributes[3].rstrip()
            keywords = cleaned.split(",")
            nodes.append(Node(id = node_id, name = name, depth = depth, keywords = keywords))
        return nodes

    def __extract_edges(self, edge_lines:list[str], node_ids:list[int]) -> set[Edge]:
        """
        Converts the saved text format into a set of edge objects

        Paramters:
        ----------
        edge_lines : list[str]
            The lines of the saved graph file that contain edge information
        
        node_ids : list[int]
            The ID's of the nodes
        """

        edges = set()
        for row_idx, edge_line in enumerate(edge_lines):
            cleaned_line = edge_line.rstrip()
            entries = cleaned_line.split(sep = " ")
            for col_idx, entry in enumerate(entries):
                if int(entry) == 0:
                    continue
                edges.add(Edge(start_id = node_ids[row_idx], end_id = node_ids[col_idx]))
        return edges

    def __read_file(self, file_name:str) -> list[str] | None:
        """
        Read the file at file_name and return the content

        Parameters:
        -----------
        file_name : str
            The file location
        """
        
        try:
            with open(file_name, "r", encoding="UTF8") as file:
                file_content = file.readlines()
        except FileNotFoundError:
            return None
        return file_content

    def __setup_folders(self) -> None:
        txtfiles_path = self.__directory + "txtfiles"
        if not os.path.isdir(txtfiles_path):
            os.mkdir(txtfiles_path)

        images_path = self.__directory + "images"
        if not os.path.isdir(images_path):
            os.mkdir(images_path)

        return None

def main()-> int:
    print("Calling main function in filehelper")
    return 0


if __name__ == "__main__":
    main()