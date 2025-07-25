from graph.graph import Graph
from graph.node import Node
from graph.edge import Edge

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

        return None
    

    def write_graph_to_file(self, graph:Graph, file_name:str) -> None:
        """
        Writes the given graph into a file at file_name in a text format

        Parameters:
        -----------
        graph : Graph
            The graph to save

        file_name : str
            The location to save to
        """

        to_write = u""
        nodes = list(graph.get_nodes())
        node_count = len(nodes)
        to_write += f"{node_count}\n"

        nodes.sort(key = lambda node : node.get_id())

        for node in nodes:
            to_write += f"{node.get_id()};{node.get_name()};{node.get_depth()};{u",".join(node.get_keywords())}\n"

        connection_matrix = [[None for _ in range(node_count)] for _ in range(node_count)]
        
        ids = [node.get_id() for node in nodes]

        for row_idx, start_id in enumerate(ids):
            out_ids = [edge.get_end_id() for edge in graph.get_node_from_id(start_id).get_outgoing()]
            for col_idx, end_id in enumerate(ids):
                if end_id in out_ids:
                    connection_matrix[row_idx][col_idx] = 1
                else:
                    connection_matrix[row_idx][col_idx] = 0

        for row in connection_matrix:
            to_write += f"{" ".join(map(str, row))}\n"

        to_write = to_write.rstrip("\n")
        with open(file_name, "x", encoding="UTF8") as file:
            file.write(to_write)
        return None
    
    def read_graph_from_file(self, file_name:str) -> Graph | None:
        """
        Reads the file at file_name and returns the saved graph

        Parameters:
        -----------
        file_name : str
            The location to read
        """

        file_content = self.__read_file(file_name = file_name)
        if file_content == None:
            return None
        
        node_count = int(file_content[0])
        node_lines = file_content[1:node_count + 1]

        nodes = self.__extract_nodes(node_lines)
        node_ids = [node.get_id() for node in nodes]

        edge_lines = file_content[node_count + 1:len(file_content)]
        edges = self.__extract_edges(edge_lines, node_ids)
        
        return Graph(nodes = nodes, edges = edges)



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

def main()-> int:
    print("Calling main function in filehelper")
    return 0


if __name__ == "__main__":
    main()