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
        return None

    
    def get_content(self, name:str, verbose:bool) -> dict[str, Any] | None:
        """
        Requests the article named name and sorts the json content into a more useful format

        Parameters:
        -----------
        name : str
            The name of the article to fetch
        """

        requester = Requester()
        response = requester.request_content(name)

        if not response:
            return None
        
        if verbose:
            report_statement = '' \
            'Request was successfull, beginning sorting of response'

            print(report_statement)

        return self.__sort_wiki_json(response, verbose)

    def __sort_wiki_json(self, response_json:dict, verbose:bool) -> dict[str, Any]:

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
        assert isinstance(page_id, int)
        sorted_entries["id"] = page_id

        wrapped_text = raw.get("text")
        assert wrapped_text
        assert isinstance(wrapped_text, dict)
        text = wrapped_text.get("*")
        assert text
        assert isinstance(text, str)
        sorted_entries["keywords"] = self.__find_keywords(text, verbose)

        wrapped_links = raw.get("links")
        assert wrapped_links
        assert isinstance(wrapped_links, list) 
        sorted_entries["links"] = self.__unwrap_links(wrapped_links, verbose)
        
        if verbose:
            report_statement = '' \
            'Response sorting done'

            print(report_statement)
        
        return sorted_entries
    
    def __unwrap_links(self, raw_links:list[dict[str, Any]], verbose:bool) -> list[str]:
        counter = 0
        unwrapped_links = []
        for entry in raw_links:
            if entry.get("ns") != 0:
                counter += 1
                continue
            raw_link = entry.get("*")
            assert raw_link
            assert isinstance(raw_link, str)
            converted_link = raw_link.replace(" ", "_")
            unwrapped_links.append(converted_link)

        if verbose:
            report_statement = '' \
            f'Got {len(raw_links)} raw links, {len(unwrapped_links)} to other wikipedia articles and {counter} others'

            print(report_statement)

        return unwrapped_links
    
    def __find_keywords(self, text:str, verbose:bool) -> list[str]:
        
        words = text.split(" ")
        cleaned_words = [word .rstrip(",.;") for word in words]
        nominals = [word for word in cleaned_words if word.isalpha() and word[0].isupper() and len(word) > 2]

        blacklist = ["Abschnitts", "Der", "Die", "Das", "Den", "Dem", "Des", "Ein", "Eine", "Einen", "Einem", "Eines", "Im", "In", "Dies", "Diese", "Dieser", "Dieses", "Er", "Sie", "Es", "Man", "Bei"]
        filtered_nominals = [nominal for nominal in nominals if nominal not in blacklist]

        frequencies = Counter(filtered_nominals).most_common()
        keywords = [entry[0] for entry in frequencies[:10]]

        if verbose:
            report_statement = '' \
            f'Found {len(words)} words, {len(nominals)} of that being nominals.\n' \
            f'Filtered out {len(nominals) - len(filtered_nominals)} common filler words.\n' \
            f'Sorting {len(filtered_nominals)} keywords and returning the 10 most used'

            print(report_statement)

        return keywords


def main() -> int:
    print("Calling main function in sorter")
    return 0


if __name__ == "__main__":
    main()