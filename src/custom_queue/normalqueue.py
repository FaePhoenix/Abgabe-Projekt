import copy
from custom_queue.queueentry import QueueEntry


class NormalQueue:
    """
    A class that is a queue of node candidates

    Attributes:
    -----------
    __entires : list[NodeQueueEntry]
        A list containing the entries of the queue

    __blacklist : list[str]
        A list containing names of articels that have been blacklisted

    
    Methods:
    --------
    get_next_entry() -> NodeQueueEntry
        Gives an entry of the queue and deletes it from the __entries

    add_article_to_blacklist(blacklisted_article : str) -> None
        Adds a given article name to the blacklist

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
        self.__blacklist:list[str] = [starting_name]
        return None


    def get_next_entry(self) -> QueueEntry | None:
        """
        Returns a queue entry, removes it from the __entries and adds it to __blacklist so it isn't explored again
        or returns None if the queue is empty
        """

        if len(self.__entries) == 0:
            return None

        next_entry = copy.deepcopy(self.__entries[0])
        self.__blacklist.append(next_entry.get_name())
        self.__entries.pop(0)

        return next_entry
    
    def add_article_to_blacklist(self, blacklisted_article:str) -> None:
        """
        Adds the given article name to __blacklist

        Parameters:
        -----------
        blacklisted_article : str
            The name of the article to be blacklisted

        """

        if blacklisted_article not in self.__blacklist:
            self.__blacklist.append(blacklisted_article)

        return None
    
    def only_update_entries(self, new_links:list[str], origin_id:int, origin_depth:int) -> None:
        """
        Updates existing queue entries by adding the given origin id to their list of discovery sources, updating the minimum discovery depth if applicable

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
        known_entries:list[str] = [entry.get_name() for entry in self.__entries]
        updatable_links = [link for link in filtered_links if link in known_entries]

        for link in updatable_links:
            self.__update_entry(link = link, origin_id = origin_id, origin_depth = origin_depth)
        
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

        filtered_links = [link for link in new_links if link not in self.__blacklist]
        known_entries:list[str] = [entry.get_name() for entry in self.__entries]

        updatable_links = [link for link in filtered_links if link in known_entries]
        
        #Duplicated Code to only_update_entries()

        for link in updatable_links:
            self.__update_entry(link = link, origin_id = origin_id, origin_depth = origin_depth)
        #end duplicate

        creatable_links = [link for link in filtered_links if link not in known_entries]

        for link in creatable_links:
            new_entry = QueueEntry(name = link, origin_id = origin_id, depth = origin_depth + 1)
            self.__entries.append(new_entry)

        return None
            
    def __update_entry(self, link:str, origin_id:int, origin_depth:int) -> None:
        """
        Updates the entry of the given article name given the source ID and depth

        Parameters:
        -----------
        link : str
            The name of the article which queue entry is to be updated

        origin_id : int
            ID of the node that is a new source

        origin_depth : int
            Depth of the node that is a new source
        """
        for entry in self.__entries:
            if entry.get_name() == link:
                entry.add_origin(origin_id = origin_id, origin_depth = origin_depth)

        return None


def main() -> int:
    return 0
    
if __name__ == "__main__":
    main()