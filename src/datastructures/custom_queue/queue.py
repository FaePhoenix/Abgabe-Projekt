from abc import ABC, abstractmethod
from datastructures.custom_queue.queueentry import QueueEntry

class WikiGraphQueue(ABC):
    """
    
    only_update_entries(new_links : list[str], origin_id : int, origin_depth : int) -> None
        Updates the already existing entries in __entries based if the are in new_links based on the origin_id and origin_depth

    add_new_entries(new_links : list[str], origin_id : int, origin_depth : int) -> None:
        Updates known articles and creates new queue entries for unknown article names in new_links based on the origin_id and origin_depth
    """
    def __init__(self, starting_name:str) -> None:
        """
        Sets up the __entries and __blacklist

        Parameters:
        -----------
        starting_name : str
            the name of the article that is used as a start of the current graph the queue object belongs to
        """

        self.__entries:list[QueueEntry] = []
        self.__blacklist:set[str] = set(starting_name)
        return None
    
    @abstractmethod
    def get_next_entry(self) -> QueueEntry | None:
        """
        Returns a queue entry, removes it from the __entries and adds it to __blacklist so it isn't explored again
        or returns None if the queue is empty
        """
        pass
    
    def add_article_to_blacklist(self, blacklisted_article:str) -> None:
        """
        Adds the given article name to __blacklist

        Parameters:
        -----------
        blacklisted_article : str
            The name of the article to be blacklisted

        """

        if blacklisted_article not in self.__blacklist:
            self.__blacklist.add(blacklisted_article)

        return None

    def only_update_entries(self, new_links:list[str], origin_id:int, origin_depth:int) -> None:
        """
        Updates existing queue entries by adding the given origin id
        to their list of discovery sources and updating the minimum discovery depth if applicable

        Parameters:
        -----------
        new_links : list[str]
            The list of article names to be updated
        
        origin_id : int
            ID of the node that is a source of the article names in new_links

        origin_depth : int
            Depth of the node that is a source of the article names in new_links
        """

        #move filtering to other function to avoid duplicated?
        filtered_links = [link for link in new_links if link not in self.__blacklist]
        known_entries = [entry.get_name() for entry in self.__entries]
        updatable_links = [link for link in filtered_links if link in known_entries]

        self.__update_entries(updatable_links, origin_id, origin_depth)
        
        return None
  
    def add_new_entries(self, new_links:list[str], origin_id:int, origin_depth:int) -> None:
        """
        Adds the article names to the queue or updates their entries if they are already present

        Parameters:
        -----------
        new_links : list[str]
            The list of article names to be added to the queue
        
        origin_id : int
            ID of the node that is a source of the article names in new_links
        
        origin_depth : int
            Depth of the node that is a source of the article names in new_links
        """

        #move filtering to other function to avoid duplicated?
        filtered_links = [link for link in new_links if link not in self.__blacklist]
        known_entries = [entry.get_name() for entry in self.__entries]
        updatable_links = [link for link in filtered_links if link in known_entries]
        
        self.__update_entries(updatable_links, origin_id, origin_depth)

        creatable_links = [link for link in filtered_links if link not in known_entries]
        self.__add_entries(creatable_links, origin_id, origin_depth)

        return None

    def __add_entries(self, links:list[str], origin_id:int, origin_depth:int) -> None:
        for link in links:
            new_entry = QueueEntry(link, origin_id, origin_depth + 1)
            self.__entries.append(new_entry)

        return None
    
    def __update_entries(self, links:list[str], origin_id:int, origin_depth:int) -> None:
        for entry in self.__entries:
            if (name := entry.get_name()) in links:
                links.remove(name)
                entry.add_origin(origin_id, origin_depth)
        return None
    