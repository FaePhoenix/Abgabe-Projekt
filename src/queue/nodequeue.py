import copy
from queue.nodequeueentry import NodeQueueEntry


class NodeQueue:
    def __init__(self, starting_name:str) -> None:
        self.__entries:list[NodeQueueEntry] = []
        self.__blacklist:list[str] = [starting_name]
        return None


    def get_next_entry(self) -> NodeQueueEntry:
        if len(self.__entries) == 0:
            raise ValueError("Queue empty")

        next_entry = copy.deepcopy(self.__entries[0])
        self.__blacklist.append(next_entry.get_name())
        self.__entries.pop(0)

        return next_entry
    
    def add_article_to_blacklist(self, blacklisted_article:str) -> None:
        self.__blacklist.append(blacklisted_article)

        return None
    
    def only_update_entries(self, new_links:list[str], origin_id:int, origin_depth:int) -> None:
        #print(f"Attempting to update {len(new_links)} entries in queue")
        filtered_links = [link for link in new_links if link not in self.__blacklist]
        known_entries:list[str] = [entry.get_name() for entry in self.__entries]
        updatable_links = [link for link in filtered_links if link in known_entries]
        #print(f"Updating {len(updatable_links)} entries in queue")

        for link in updatable_links:
            self.__update_entry(link = link, origin_id = origin_id, origin_depth = origin_depth)
        
        return None

    def add_new_entries(self, new_links:list[str], origin_id:int, origin_depth:int) -> None:

        filtered_links = [link for link in new_links if link not in self.__blacklist]
        known_entries:list[str] = [entry.get_name() for entry in self.__entries]

        updatable_links = [link for link in filtered_links if link in known_entries]

        for link in updatable_links:
            self.__update_entry(link = link, origin_id = origin_id, origin_depth = origin_depth)

        creatable_links = [link for link in filtered_links if link not in known_entries]

        for link in creatable_links:
            new_entry = NodeQueueEntry(name = link, origin_id = origin_id, depth = origin_depth + 1)
            self.__entries.append(new_entry)

        self.__entries.sort(key = lambda entry : entry.get_degree(), reverse = True)


        return None
            
    def __update_entry(self,link:str, origin_id:int, origin_depth:int) -> None:
        for entry in self.__entries:
            if entry.get_name() == link:
                entry.add_origin(origin_id = origin_id, origin_depth = origin_depth)

        return None


def main() -> int:
    return 0
    
if __name__ == "__main__":
    main()