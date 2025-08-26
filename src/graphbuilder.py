from custom_queue.priorityqueue import PriorityQueue
from custom_queue.queueentry import QueueEntry
from fetch.sorter import Sorter
from graph.graph import Graph
from graph.node import Node
from graph.edge import Edge
from typing import Any


class GraphBuilder:
    def __init__(self, max_graph_size:int = 500, max_depth:int = 10) -> None:
        self.__max_graph_size:int = max_graph_size
        self.__max_depth:int = max_depth
        self.__edges:list[Edge] = []
        self.__nodes:dict[str, Node] = {}
        self.__queue:PriorityQueue
        return None
    
    def build_graph_from_article(self, start_name:str) -> Graph | None:
        sorter = Sorter()
        self.__queue = PriorityQueue(starting_name = start_name)

        try:
            starting_info = sorter.get_content(start_name)
        except AssertionError:
            #print(f"Aborting graph construction, because inital article \"{start_name}\" could not be found.")
            return None
        
        starting_id = starting_info.get("id")
        starting_name = starting_info.get("name")
        self.__add_node(node_id = starting_id, node_name = starting_name, node_data = starting_info.get("keywords"), node_depth = 0)

        self.__queue.add_new_entries(new_links = starting_info.get("links"), origin_id = starting_id, origin_depth = 0)

        while len(self.__nodes) < self.__max_graph_size:
            #print(f"Current amount of existing nodes: {len(self.__nodes)}")
            
            next_queue_entry = self.__queue.get_next_entry()
            
            if next_queue_entry == None:
                break

            article_name = next_queue_entry.get_name()
            article_depth = next_queue_entry.get_depth()
            
            try:
                new_info = sorter.get_content(article_name)

            except (AssertionError, AttributeError):
                print(f"Blacklisting {article_name}")
                self.__queue.add_article_to_blacklist(blacklisted_article = article_name)
                continue

            article_id = new_info.get("id")
            self.__add_node(node_id = article_id, node_name = article_name, node_data = new_info.get("keywords"), node_depth = article_depth)
            self.__add_edges_toward_node(id_list = next_queue_entry.get_origins(), node_id = article_id)

            self.__build_edges_from_links(next_queue_entry, article_depth, new_info, article_id)

        network = Graph(root = start_name, nodes = list(self.__nodes.values()), edges = self.__edges)

        return network

    def __build_edges_from_links(self, next_queue_entry:QueueEntry, article_depth:int, new_info:dict[str, Any], article_id:int) -> None:
        links = new_info.get("links")

        new_links = []
        build_links = []
        
        for link in links:
            if link in self.__nodes.keys():
                build_links.append(link)
            else: 
                new_links.append(link)

        self.__build_egdes_to_existing_nodes(article_id, build_links)
        self.__update_queue_from_links(next_queue_entry, article_depth, article_id, new_links)

        return None

    def __update_queue_from_links(self, next_queue_entry:QueueEntry, article_depth:int, article_id:int, new_links:list[str]) -> None:
        if next_queue_entry.get_depth() < self.__max_depth:
            self.__queue.add_new_entries(new_links, article_id, article_depth)

        else:
            self.__queue.only_update_entries(new_links, article_id, article_depth)

        return None

    def __build_egdes_to_existing_nodes(self, article_id:int, build_links:list[str]) -> None:
        ids = [node.get_id() for node in self.__nodes.values() if node.get_name() in build_links]

        for id in ids:
            new_edge = Edge(article_id, id)
            self.__edges.append(new_edge)

        return None

    def __add_node(self, node_id:int, node_name:str, node_data:list[str], node_depth:int) -> None:
        new_node = Node(id = node_id, name = node_name, keywords = node_data, depth = node_depth)
        self.__nodes[node_name] = new_node

        return None

    def __add_edges_toward_node(self, id_list:list[int], node_id:int) -> None:
        for connection_id in id_list:
            new_edge = Edge(start_id = connection_id, end_id = node_id)
            self.__edges.append(new_edge)

        return None


def main() -> int:
    print("Calling main function in graphbuilder")
    return 0


if __name__ == "__main__":
    main()