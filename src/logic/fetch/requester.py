import requests


class Requester:
    """
    A class to encapsulates methods to request content from the wikipedia api

    Methods:
    --------
    request_content(articlename : str) -> dict
        Fetches the wiki article which name is given by articlename if it exists and returns it's json content
    """


    def __init__(self) -> None:
        """
        Setup of the object
        """

        return None
    

    def request_content(self, article_name:str) -> dict:
        """
        Fetches the article named articlename if it exisits and returns it's json content

        Parameters:
        -----------
        article_name : str
            The name of the article to fetch
        """

        raw_response = self.__get_wikiapi_response(article_name)
        return self.__get_content_from_response(raw_response)

    def __get_wikiapi_response(self, article_name:str) -> requests.Response:
        """
        Requests the json content of a wikipage and asserts that it exists

        Parameters:
        -----------
        article_name : str
            The name of the article
        """

        user_agent = "WikiGraphUniProject/0.1 (fae.koerper@uni-jena.de) bot"
        headers = {'User-Agent' : user_agent}

        wiki_api_domain = "https://de.wikipedia.org/w/api.php?action=parse&format=json&page="
        full_link = wiki_api_domain + article_name

        response = requests.get(url = full_link, headers = headers)

        response_code = response.status_code
        assert response_code == requests.codes.ok, f"Status code is {response_code} not 200"

        return response

    def __get_content_from_response(self, response:requests.Response) -> dict:
        """
        Extracts the json content in form of a dict from the response object

        Parameters:
        -----------
        response : requests.Response
            The response object
        """
        
        return response.json()


def main() -> int:
    print("Calling main function in requester")
    return 0


if __name__ == "__main__":
    main()