import requests
import json

class WildBerriesParser():
    
    def __init__(self, ab_testing: bool = False, appType: int = 1, curr: str = "rub",
                 dest: int = -1257786, hide_vflags: int = 4294967296, lang: str = "ru", resultset: str = "catalog",
                 sort: str = "popular", spp: int = 30, suppressSpellcheck: bool = False) -> None:
        
        self.__url = "https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search"
        
        self._cookie = {
        "x_wbaas_token": ""
        }
        self._params = {
            "ab_testing": ab_testing,
            "appType": appType,
            "curr": curr,
            "dest": dest,
            "hide_vflags": hide_vflags,
            "lang": lang,
            "page": None,
            "query": None,
            "resultset": resultset,
            "sort": sort,
            "spp": spp,
            "suppressSpellcheck": suppressSpellcheck
        }
        self.__session = requests.Session()
        
    def set_cookie(self, token):
        self._cookie["x_wbaas_token"] = token

    def parse_page(self, url):
        with self.__session as session:
            session.params = self._params
            response = session.get(url, cookies=self._cookie)
            response_json = response.json()
            description = response_json.get("description")
            

    def parse_products(self, query: str, page: int):
        products = self._request(query, page)
        filter_profucts = []
        for product in products:
            data = {}
            data["url_card"] = f"https://www.wildberries.ru/catalog/{product["id"]}/detail.aspx"
            data["id"] = product["id"]
            data["name"] = product["name"]
            data["reviewRating"] = product["reviewRating"]
            data["reviews"] = product["feedbacks"]
            data["price"] = product["sizes"][0]["price"]["product"]
            data["seller"] = product["brand"]
            data["page_seller"] = f"https://www.wildberries.ru/seller/{product["supplierId"]}"
            for size in product["sizes"]:
                data.setdefault("size", []).append(size["name"])
            filter_profucts.append(data)
        print(filter_profucts)

    def _request(self, query: str, page: int):
        with self.__session as session:
            self._params["query"] = query
            self._params["page"] = page
            session.params = self._params
            response = session.get(self.__url, cookies=self._cookie)
            if response.status_code == 498:
                raise requests.RequestException("Не установлен cookie x_wbaas_token")
            response_json = response.json()
            products = response_json.get("products")
            total: int = response_json.get("total")
            
            if (products is None or len(products) == 0) and total // 100 + 1 < page:
                raise requests.RequestException("Страницы не существует")
            
            return products

if __name__ == "__main__":
    import dotenv
    import os
    
    dotenv.load_dotenv()
    token = os.getenv("X_WBAAS_TOKEN")
    
    parser = WildBerriesParser()
    parser.set_cookie(token)
    parser.parse_products("тарелки стеклянные", 1)