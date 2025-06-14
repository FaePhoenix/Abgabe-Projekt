from fetch.requester import Requester
from collections import Counter

class Sorter:
    def __init__(self) -> None:
        return None

    
    def get_content(self, name:str) -> dict:
        requester = Requester()
        response = requester.request_content(articlename = name)
        return self.__sort_wiki_json(response_json = response)

    def __sort_wiki_json(self, response_json:dict) -> dict:
        raw = response_json.get("parse")
        if raw == None:
            print(f"Gewaltiges Problem:\n{response_json}")
        sorted = {}

        sorted["name"] = raw.get("title")
        sorted["id"] = raw.get("pageid")
        raw_text = raw.get("text").get("*")
        sorted["keywords"] = self.__find_keywords(text = raw_text)

        links_wrapped = raw.get("links")
        sorted["links"] = self.__unwrap_links(raw_links = links_wrapped)

        return sorted
    
    def __unwrap_links(self, raw_links:list) -> list:
        unwrapped_links = []
        for entry in raw_links:
            if entry.get("ns") != 0:
                continue
            raw_link = entry.get("*")
            converted_link = raw_link.replace(" ", "_")
            unwrapped_links.append(converted_link)
        return unwrapped_links
    
    def __find_keywords(self, text:str) -> str:
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