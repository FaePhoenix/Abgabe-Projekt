from datastructures.custom_queue.priorityqueue import PriorityQueue
from datastructures.custom_queue.normalqueue import NormalQueue
from datastructures.custom_queue.queue import WikiGraphQueue
from datastructures.graph.graph import Graph
from datastructures.graph.node import Node
from datastructures.graph.edge import Edge

from logic.fetch.sorter import Sorter

from typing import Any


class GraphBuilder:
    """
    A class to organize the creation of new graphs by fetching and organizing data

    Attributes:
    -----------
    __max_graph_size : int
        The maximum size of the graph that is being created

    __max_depth : int
        The maximum distance that an article can have to the root

    __edges : set[Edge]
        The collection of created edges

    __nodes : dict[str, Node]
        The collection of created nodes accessable by article name

    __queue : WikiGraphQueue
        The queue that holds the seen but not accessed articles

    Methods:
    --------
    build_graph_from_article(start_name : str, queue_type : str, verbose : bool) -> Graph | None
        Returns the created graph or None if creation failed
    """

    def __init__(self, max_graph_size:int, max_depth:int) -> None:
        """
        Sets up the object

        Parameters:
        -----------
        max_graph_size : int
            The maximum graph size to build

        max_depth : int
            The maximum distance to the root article to consider during graph building
        """

        self.__max_graph_size:int = max_graph_size
        self.__max_depth:int = max_depth
        self.__edges:set[Edge] = set()
        self.__nodes:dict[str, Node] = {}
        self.__queue:WikiGraphQueue
        return None
    
    def build_graph_from_article(self, start_name:str, queue_type:str, verbose:bool) -> Graph | None:
        """
        Builds a graph from the article given by start_name as root and then fetching
        and adding new nodes until either the queue is empty or the maximum size is reached

        Parameters:
        -----------
        start_name : str
            The name of the root article

        queue_type : str
            The type of queue to use (normal or priority)

        verbose : bool
            If the action should be logged verbosely
        """

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
        if not (starting_id and isinstance(starting_id, int)):
            warning_statement = '' \
            'Could not read ID from article.\n' \
            'Aborting'

            print(warning_statement)
            return None

        starting_name = starting_info.get("name")
        if not (starting_name and isinstance(starting_name, str)):
            warning_statement = '' \
            'Could not read name from article.\n' \
            'Aborting'

            print(warning_statement)
            return None

        starting_keywords = starting_info.get("keywords")
        if not (starting_keywords and isinstance(starting_keywords, list)):
            warning_statement = '' \
            'Could not read keywords from article.\n' \
            'Aborting'

            print(warning_statement)
            return None
 
        self.__add_node(starting_id, starting_name, starting_keywords, 0)

        starting_links = starting_info.get("links")
        if not (starting_links and isinstance(starting_links, list)):
            warning_statement = '' \
            'Could not read links from article.\n' \
            'Aborting'

            print(warning_statement)
            return None

        report_statement = f'\n(1|{self.__max_graph_size})'

        if verbose:
            report_statement += f'Built root node and found id {starting_id} and {len(starting_links)} new links'
            
        print(report_statement)
        
        self.__queue.add_new_entries(starting_links, starting_id, 0, verbose)

        self.__run_build_loop(sorter, verbose)

        if verbose:
            report_statement = '' \
            'Graph creation finished.'

            print(report_statement)

        network = Graph(start_name, set(self.__nodes.values()), self.__edges)

        return network

    def __run_build_loop(self, sorter:Sorter, verbose:bool) -> None:
        """
        The main loop to build a graph to request an article, add the content to the graph
        and extend the queue with the found links

        Parameters:
        -----------
        sorter : Sorter
            The object to request articles with

        verbose : bool
            Should the action be logged verbosely
        """

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
            
        return None

    def __build_edges_from_links(self, article_depth:int, new_info:dict[str, Any], article_id:int, verbose:bool) -> None:
        """
        Creating edges for the graph from the links

        Parameters:
        -----------
        article_depth : int
            The article depth of the link source

        new_info : dict[str, Any]
            The sorted information from  the article
        
        article_id : int
            The id of the source article

        verbose : bool
            Should the action be logged verbosely
        """

        new_links = []
        build_links = []
        
        links = new_info.get("links")
        assert links != None
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
        """
        Update the queue from links and add new entries for new links

        Parameters:
        -----------
        article_depth : int
            The depth of the source article

        article_id : int
            The id of the source article

        new_links : list[str]
            The links to update the queue

        verbose : bool
            Should the action be logged verbosely
        """

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
        """
        Only updating the queue from the given queue

        Parameters:
        -----------
        article_id : int
            The id of the source article

        build_links : list[str]
            The links to update from

        verbose : bool
            Should the action be logged verbosely
        """
        
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
        """
        Adding a new node

        Parameters:
        -----------
        node_id : int
            The id of the article

        node_name : int
            The name of the article

        node_data : list[str]
            The keywords of the article

        node_depth : int
            The depth of the article
        """

        new_node = Node(id = node_id, name = node_name, keywords = node_data, depth = node_depth)

        self.__nodes[node_name] = new_node

        return None

    def __add_edges_toward_node(self, id_list:list[int], node_id:int, verbose:bool) -> None:
        """
        Adding edges towards a node

        Parameters:
        -----------
        id_list : list[int]
            The id's of nodes that link towards the article

        node_id : int
            The id of the node

        verbose : bool
            Should the action be logged verbosely
        """

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