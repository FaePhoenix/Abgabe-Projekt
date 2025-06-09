from queue.nodequeue import NodeQueue
from fetch.sorter import Sorter
from graph.graph import Graph
from graph.node import Node
from graph.edge import Edge
import time


class GraphBuilder:
    def __init__(self, max_graph_size:int = 500, max_depth:int = 10) -> None:
        self.__max_graph_size:int = max_graph_size
        self.__max_depth:int = max_depth
        self.__edges:list[Edge] = []
        self.__nodes:list[Node] = []
        return None
    
    def build_graph_from_article(self, start_name:str) -> Graph:
        sorter = Sorter()
        queue = NodeQueue(starting_name = start_name)

        try:
            starting_info = sorter.get_content(start_name)
        except AssertionError:
            #print(f"Aborting graph construction, because inital article \"{start_name}\" could not be found.")
            return Graph()
        
        starting_id = starting_info.get("id")
        self.__add_node(node_id = starting_id, node_name = starting_info.get("name"), node_data = starting_info.get("keywords"), node_depth = 0)
        queue.add_new_entries(new_links = starting_info.get("links"), origin_id = starting_id, origin_depth = 0)

        while len(self.__nodes) < self.__max_graph_size:
            print(f"Current amount of existing nodes: {len(self.__nodes)}")
            try:
                next = queue.get_next_entry()

            except ValueError:
                #print(f"Exiting Graph creation as no further connections have been found.")
                break
            
            article_name = next.get_name()
            article_depth = next.get_depth()
            #print(f"Attempting to get article: {article_name}\nFirst seen in:{next.get_origins()[0]}, last seen in: {next.get_origins()[-1]}")
            
            request_start = time.time()
            try:
                new_info = sorter.get_content(article_name)

            except AssertionError:
                #print(f"Can't find article \"{article_name}\". Skipping and adding to blacklist")
                queue.add_article_to_blacklist(blacklisted_article = article_name)
                continue
            request_end = time.time()

            node_start = time.time()
            article_id = new_info.get("id")
            self.__add_node(node_id = article_id, node_name = article_name, node_data = new_info.get("keywords"), node_depth = article_depth)
            self.__add_edges_toward_node(id_list = next.get_origins(), node_id = article_id)
            node_end = time.time()

            links = new_info.get("links")

            queue_start = time.time()
            if next.get_depth() < self.__max_depth:
                queue.add_new_entries(new_links = links, origin_id = article_id, origin_depth = article_depth)
            else:
                queue.only_update_entries(new_links = links, origin_id = article_id, origin_depth = article_depth)
            queue_end = time.time()

            request_time = request_end - request_start
            node_time = node_end - node_start
            queue_time = queue_end - queue_start
            time_sum = request_time + node_time + queue_time
            print(f"Took {format(time_sum*1000, ".6f")}ms: Request {format(request_time/time_sum * 100, ".4f")}%, Node {format(node_time/time_sum * 100, ".4f")}%, Queue {format(queue_time/time_sum * 100, ".4f")}%")


        network = Graph(nodes = self.__nodes, edges = self.__edges)

        return network

    def __add_node(self, node_id:int, node_name:str, node_data:list[str], node_depth:int) -> None:
        #print(f"Adding new Node\nid: {node_id}, name: {node_name}, depth: {node_depth}")
        new_node = Node(id = node_id, name = node_name, keywords = node_data, depth = node_depth)
        self.__nodes.append(new_node)
        return None

    def __add_edges_toward_node(self, id_list:list[int], node_id:int) -> None:
        #print(f"Adding {len(id_list)} new edges")
        for connection_id in id_list:
            new_edge = Edge(start_id = connection_id, end_id = node_id)
            self.__edges.append(new_edge)

        return None


def main() -> int:
    print("Calling main function in graphbuilder")
    return 0


if __name__ == "__main__":
    main()