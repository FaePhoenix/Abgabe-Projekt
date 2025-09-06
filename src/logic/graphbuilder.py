from datastructures.custom_queue.priorityqueue import PriorityQueue
from datastructures.custom_queue.normalqueue import NormalQueue
from datastructures.custom_queue.queue import WikiGraphQueue
from datastructures.custom_queue.queueentry import QueueEntry
from logic.fetch.sorter import Sorter
from datastructures.graph.graph import Graph
from datastructures.graph.node import Node
from datastructures.graph.edge import Edge
from typing import Any


class GraphBuilder:
    def __init__(self, max_graph_size, max_depth) -> None:
        self.__max_graph_size:int = max_graph_size
        self.__max_depth:int = max_depth
        self.__edges:set[Edge] = set()
        self.__nodes:dict[str, Node] = {}
        self.__queue:WikiGraphQueue
        return None
    
    def build_graph_from_article(self, start_name:str, queue_type:str, verbose:bool) -> Graph | None:
        sorter = Sorter()

        assert queue_type in ["n", "p"]
        match queue_type:
            case "n":
                self.__queue = NormalQueue(start_name)
            case "p":
                self.__queue = PriorityQueue(start_name)


        if verbose:
            request_statement = '' \
            f'Requesting root article \"{start_name}\" from wikipedia'

            print(request_statement)

        starting_info = sorter.get_content(start_name, verbose)

        if not starting_info:
            failure_statement = '' \
            'Did not recieve wikipedia article for root.\n' \
            'Aborting graph building'

            print(failure_statement)
            return None
       
        starting_id = starting_info.get("id")
        assert starting_id
        assert isinstance(starting_id, int)

        starting_name = starting_info.get("name")
        assert starting_name
        assert isinstance(starting_name, str)

        starting_keywords = starting_info.get("keywords")
        assert starting_keywords
        assert isinstance(starting_keywords, list)
        self.__add_node(starting_id, starting_name, starting_keywords, 0)

        starting_links = starting_info.get("links")
        assert starting_links
        assert isinstance(starting_links, list)

        report_statement = f'\n(1|{self.__max_graph_size})'

        if verbose:
            report_statement += f'Built root node and found id {starting_id} and {len(starting_links)} new links'
            
        print(report_statement)
        
        self.__queue.add_new_entries(starting_links, starting_id, 0, verbose)

        while len(self.__nodes) < self.__max_graph_size:
            
            next_queue_entry = self.__queue.get_next_entry()

            if next_queue_entry == None:
                end_statement = '' \
                'Ending graph building early as queue is empty'

                print(end_statement)
                break

            article_name = next_queue_entry.get_name()
            article_depth = next_queue_entry.get_depth()
            
            if verbose:
                report_statement = '' \
                f'\nNext queue entry: {article_name} at depth {article_depth}'

                print(report_statement)
            
            new_info = sorter.get_content(article_name, verbose)

            if not new_info:
                warning_statement = '' \
                f'Failed to get wikipedia article for {article_name}\n' \
                'Skipping and blacklisting'

                self.__queue.add_article_to_blacklist(article_name)
                print(warning_statement)
                continue

            article_id = new_info.get("id")
            assert article_id
            assert isinstance(article_id, int)

            new_keywords = new_info.get("keywords")
            assert new_keywords
            assert isinstance(new_keywords, list)

            report_statement = '' \
            f'({len(self.__nodes.items()) + 1}|{self.__max_graph_size})'

            if verbose:
                report_statement += f'Adding Node \"{article_name}\" with id {article_id}'
                
            print(report_statement)
            
            self.__add_node(article_id, article_name, new_keywords, article_depth)
            self.__add_edges_toward_node(next_queue_entry.get_origins(), article_id, verbose)

            self.__build_edges_from_links(article_depth, new_info, article_id, verbose)

        if verbose:
            report_statement = '' \
            'Graph creation finished.'

            print(report_statement)

        network = Graph(start_name, set(self.__nodes.values()), self.__edges)

        return network

    def __build_edges_from_links(self, article_depth:int, new_info:dict[str, Any], article_id:int, verbose:bool) -> None:
        new_links = []
        build_links = []
        
        links = new_info.get("links")
        assert links
        assert isinstance(links, list)

        if verbose:
            report_statement = '' \
            f'Found {len(links)} outgoing links from node'

            print(report_statement)
        
        for link in links:
            if link in self.__nodes.keys():
                build_links.append(link)
            else: 
                new_links.append(link)

        self.__build_egdes_to_existing_nodes(article_id, build_links, verbose)

        
        self.__update_queue_from_links(article_depth, article_id, new_links, verbose)

        return None

    def __update_queue_from_links(self, article_depth:int, article_id:int, new_links:list[str], verbose:bool) -> None:
        if verbose:
            report_statement = '' \
            f'Found {len(new_links)} links to unkown nodes'

            print(report_statement)
        
        if article_depth < self.__max_depth:
            self.__queue.add_new_entries(new_links, article_id, article_depth, verbose)

        else:
            if verbose:
                report_statement = '' \
                'Article was at max depth. Only updating existing queue entries and not adding new entries'

                print(report_statement)
            self.__queue.only_update_entries(new_links, article_id, article_depth, verbose)

        return None

    def __build_egdes_to_existing_nodes(self, article_id:int, build_links:list[str], verbose:bool) -> None:
        if verbose:
            report_statement = '' \
            f'Found {len(build_links)} links to existing nodes and building edges'

            print(report_statement)
        
        ids = [node.get_id() for node in self.__nodes.values() if node.get_name() in build_links]

        for id in ids:
            new_edge = Edge(article_id, id)
            self.__edges.add(new_edge)

        return None

    def __add_node(self, node_id:int, node_name:str, node_data:list[str], node_depth:int) -> None:
        new_node = Node(id = node_id, name = node_name, keywords = node_data, depth = node_depth)
        self.__nodes[node_name] = new_node

        return None

    def __add_edges_toward_node(self, id_list:list[int], node_id:int, verbose:bool) -> None:
        if verbose:
            report_statement = '' \
            f'Adding {len(id_list)} edges from existing nodes toward current node.'

            print(report_statement)
        
        for connection_id in id_list:
            new_edge = Edge(start_id = connection_id, end_id = node_id)
            self.__edges.add(new_edge)

        return None


def main() -> int:
    print("Calling main function in graphbuilder")
    return 0


if __name__ == "__main__":
    main()