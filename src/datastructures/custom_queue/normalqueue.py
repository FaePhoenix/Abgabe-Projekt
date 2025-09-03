from datastructures.custom_queue.queueentry import QueueEntry
from datastructures.custom_queue.queue import WikiGraphQueue

class NormalQueue(WikiGraphQueue):
    """
    A class that is a queue of node candidates, inheriting from WikiGraphQueue

    Methods:
    --------
    get_next_entry() -> NodeQueueEntry
        Gives an entry of the queue and deletes it from the __entries
    """


    def __init__(self, starting_name:str) -> None:
        """
        Sets up the __entries and __blacklist

        Parameters:
        -----------
        starting_name : str
            the name of the article that is used as a start of the current graph the queue object belongs to
        """

        super().__init__(starting_name)
        return None


    def get_next_entry(self) -> QueueEntry | None:
        """
        Returns a queue entry, removes it from the __entries and adds it to __blacklist so it isn't explored again
        or returns None if the queue is empty
        """

        if len(self.__entries) == 0:
            return None

        next_entry = self.__entries.pop(0)
        self.__blacklist.add(next_entry.get_name())
        
        return next_entry


def main() -> int:
    return 0

  
if __name__ == "__main__":
    main()