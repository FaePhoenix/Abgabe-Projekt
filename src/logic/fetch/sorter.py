from logic.fetch.requester import Requester

import re
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

        self.requester = Requester()
        return None

    def get_content(self, name:str, verbose:bool) -> dict[str, Any] | None:
        """
        Requests the article named name and sorts the json content into a more useful format

        Parameters:
        -----------
        name : str
            The name of the article to fetch

        verbose : bool
            Should the action be logged verbosely
        """

        response = self.requester.request_content(name)

        if not response:
            return None
        
        if verbose:
            report_statement = '' \
            'Got response from wikipedia, beginning sorting of response'

            print(report_statement)

        return self.__sort_wiki_json(response, verbose)

    def __sort_wiki_json(self, response_json:dict, verbose:bool) -> dict[str, Any] | None:
        """
        Read content from json response into dict format

        Parameters:
        -----------
        response_json : dict
            The whole json response

        verbose : bool
            Should the action be logged verbosely
        """

        raw = response_json.get("parse")

        if not raw:
            failure_statement = '' \
            'Recieved content from wikipedia but not in the expected format.\n' \
            'Can\'t read article'

            print(failure_statement)
            return None
        
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

        sorted_entries["links"] = self.__unwrap_links(text, verbose)
        
        if verbose:
            report_statement = '' \
            'Response sorting done\n'

            print(report_statement)
        
        return sorted_entries
    
    def __unwrap_links(self, article_text:str, verbose:bool) -> list[str]:
        """
        Read links out of given article text

        Paramters:
        ----------
        article_text : str
            The article text

        verbose : bool
            Should the action be logged verbosely
        """

        link_pattern = r'<a href="/wiki/(.+?)".+?>.+?<\/a>'
        link_matches = re.findall(link_pattern, article_text)

        filtered_matches = [match for match in link_matches if "Datei:" not in match and "Spezial:" not in match]
        section_trim_pattern = r'([^#]+?)(#.+)'
        trimmed_matches = [re.match(section_trim_pattern, match) for match in filtered_matches]

        filtered_trimmed_matches = [match.group(1) for match in trimmed_matches if match]

        if verbose:
            report_statement = '' \
            f'Found {len(filtered_trimmed_matches)} links to other articles'

            print(report_statement)

        return filtered_trimmed_matches
    
    def __find_keywords(self, text:str, verbose:bool) -> list[str]:
        """
        Reading the kexwords out of the article text

        Parameters:
        -----------
        text : str
            The article text

        verbose : bool
            Should the action be logged verbosely
        """

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