from logic.fetch.requester import Requester
from collections import Counter
from typing import Any


class Sorter:
    """
    A class to encapsulate functions to convert the json response of the wiki api into a more useful format for further use

    Methods:
    --------
    get_content(name : str) -> dict[str, Any]
        Requests the article named name and sorts the json content into a more useful format    
    """


    def __init__(self) -> None:
        """
        Sets up the object
        """

        return None

    
    def get_content(self, name:str) -> dict[str, Any]:
        """
        Requests the article named name and sorts the json content into a more useful format

        Parameters:
        -----------
        name : str
            The name of the article to fetch
        """

        requester = Requester()
        response = requester.request_content(article_name = name)
        return self.__sort_wiki_json(response_json = response)

    def __sort_wiki_json(self, response_json:dict) -> dict[str, Any]:
        """
        Sorts the json content into a new dict

        Parameters:
        -----------
        response_json : dict
            The response json of the wiki api
        """

        raw = response_json.get("parse")
        assert raw
        assert isinstance(raw, dict)
        sorted_entries:dict[str, Any] = {}

        title = raw.get("title")
        assert title
        assert isinstance(title, str)
        sorted_entries["name"] = title

        page_id = raw.get("pageid")
        assert page_id
        assert isinstance(page_id, int) #TODO may be str? figure out
        sorted_entries["id"] = page_id

        wrapped_text = raw.get("text")
        assert wrapped_text
        assert isinstance(wrapped_text, dict)
        text = wrapped_text.get("*")
        assert text
        assert isinstance(text, str)
        sorted_entries["keywords"] = self.__find_keywords(text)

        wrapped_links = raw.get("links")
        assert wrapped_links
        assert isinstance(wrapped_links, list) # TODO better test type?
        sorted_entries["links"] = self.__unwrap_links(wrapped_links)

        return sorted_entries
    
    def __unwrap_links(self, raw_links:list[dict[str, Any]]) -> list[str]:
        """
        Extracts the links from the json into a more practical format

        Parameters:
        -----------
        raw_links : list[dict[str, Any]]
            The json containing the links 
        """

        unwrapped_links = []
        for entry in raw_links:
            if entry.get("ns") != 0:
                continue
            raw_link = entry.get("*")
            assert raw_link
            assert isinstance(raw_link, str) # TODO CHECK if correct type
            converted_link = raw_link.replace(" ", "_")
            unwrapped_links.append(converted_link)
        return unwrapped_links
    
    def __find_keywords(self, text:str) -> list[str]:
        """
        Extracts the keywords out of an article

        Parameters:
        -----------
        text : str
            The text of the article
        """
        
        words = text.split(" ")
        cleaned_words = [word .rstrip(",.;") for word in words]
        nominals = [word for word in cleaned_words if word.isalpha() and word[0].isupper() and len(word) > 2]

        blacklist = ["Abschnitts", "Der", "Die", "Das", "Den", "Dem", "Des", "Ein", "Eine", "Einen", "Einem", "Eines", "Im", "In", "Dies", "Diese", "Dieser", "Dieses", "Er", "Sie", "Es", "Man", "Bei"]
        filtered_nominals = [nominal for nominal in nominals if nominal not in blacklist]

        frequencies = Counter(filtered_nominals).most_common()
        keywords = [entry[0] for entry in frequencies[:10]]

        return keywords


def main() -> int:
    print("Calling main function in sorter")
    return 0


if __name__ == "__main__":
    main()