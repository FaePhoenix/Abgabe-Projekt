import requests


class Requester:
    def __init__(self) -> None:
        return
    

    def request_content(self, articlename:str) -> dict:
        raw_response = self.__get_wikiapi_response(articlename)
        return self.__get_content_from_response(raw_response)

    def __get_wikiapi_response(self, article_name:str) -> requests.Response:
        wiki_api_domain = "https://de.wikipedia.org/w/api.php?action=parse&format=json&page="
        full_link = wiki_api_domain + article_name

        response = requests.get(full_link)

        response_code = response.status_code
        assert response_code == requests.codes.ok, f"Status code is {response_code} not 200"

        return response

    def __get_content_from_response(self, response:requests.Response) -> dict:
        return response.json()


def main() -> int:
    print("Calling main function in requester")
    return 0


if __name__ == "__main__":
    main()