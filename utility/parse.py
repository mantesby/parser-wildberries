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
            
    def _find_basket(self, card_id):
        part = card_id // 1000
        vol = card_id // 100000
        
        for i in range(36, 60):
            url = f"https://basket-{i}.wbbasket.ru/vol{vol}/part{part}/{card_id}/images/hq/1.webp"
            response = self.__session.get(url)
            print(i, response.status_code)
            if response.status_code == 200:
                return i
        
        raise requests.HTTPError("Слишком много http запросов")
    
    def _get_basket(self, card_id: int):
        vol = card_id // 100000
        if vol <= 143: return '01'
        elif vol >= 144 and vol <= 287: return '02'
        elif vol >= 288 and vol <= 431: return '03'
        elif vol >= 432 and vol <= 719: return '04'
        elif vol >= 720 and vol <= 1007: return '05'
        elif vol >= 1008 and vol <= 1061: return '06'
        elif vol >= 1062 and vol <= 1115: return '07'
        elif vol >= 1116 and vol <= 1169: return '08'
        elif vol >= 1170 and vol <= 1313: return '09'
        elif vol >= 1314 and vol <= 1601: return '10'
        elif vol >= 1602 and vol <= 1655: return '11'
        elif vol >= 1656 and vol <= 1919: return '12'
        elif vol >= 1920 and vol <= 2045: return '13'
        elif vol >= 2046 and vol <= 2189: return '14'
        elif vol >= 2190 and vol <= 2405: return '15'
        elif vol >= 2406 and vol <= 2621: return '16'
        elif vol >= 2622 and vol <= 2837: return '17'
        elif vol >= 2838 and vol <= 3053: return '18'
        elif vol >= 3054 and vol <= 3269: return '19'
        elif vol >= 3270 and vol <= 3485: return '20'
        elif vol >= 3486 and vol <= 3701: return '21'
        elif vol >= 3702 and vol <= 3917: return '22'
        elif vol >= 3918 and vol <= 4133: return '23'
        elif vol >= 4134 and vol <= 4349: return '24'
        elif vol >= 4350 and vol <= 4555: return '25'
        elif vol >= 4566 and vol <= 4877: return '26'
        elif vol >= 4878 and vol <= 5189: return '27'
        elif vol >= 5190 and vol <= 5501: return '28'
        elif vol >= 5502 and vol <= 5813: return '29'
        elif vol >= 5814 and vol <= 6125: return '30'
        elif vol >= 6126 and vol <= 6437: return '31'
        elif vol >= 6438 and vol <= 6749: return '32'
        elif vol >= 6750 and vol <= 7061: return '33'
        elif vol >= 7062 and vol <= 7373: return '34'
        elif vol >= 7374 and vol <= 7687: return '35'
        else: return self._find_basket(card_id)
                
    def _request_page_img(self, card_id: int, count_img: int):
        basket_shard = self._get_basket(card_id)
        part = card_id // 1000
        vol = card_id // 100000
        urls_image = []
        for i in range(1, count_img + 1):
            urls_image.append(f"https://basket-{basket_shard}.wbbasket.ru/vol{vol}/part{part}/{card_id}/images/big/{i}.webp")
        return urls_image

    def _request_page_info(self, card_id: int):
        with self.__session as session:
            basket_shard = self._get_basket(card_id)
            part = card_id // 1000
            vol = card_id // 100000
            url = f"https://basket-{basket_shard}.wbbasket.ru/vol{vol}/part{part}/{card_id}/info/ru/card.json"
            response = session.get(url, cookies=self._cookie)
            data_response = response.json()
            data_card = {
                "description": data_response["description"],
                "main_info": data_response["grouped_options"][0],
                "additional_info": data_response["grouped_options"][1]
            }
            return data_card

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
            data["total"] = product["totalQuantity"]
            for size in product["sizes"]:
                data.setdefault("size", []).append(size["name"])
            data_page = self._request_page_info(product["id"])
            urls_image_card = self._request_page_img(product["id"], product["pics"])
            data["description"] = data_page["description"]
            data["main_info"] = data_page["main_info"]
            data["additional_info"] = data_page["additional_info"]
            data["pics"] = urls_image_card
            filter_profucts.append(data)
            break
        print(filter_profucts)

    def _request(self, query: str, page: int):
        with self.__session as session:
            self._params["query"] = query
            self._params["page"] = page
            response = session.get(self.__url, params=self._params, cookies=self._cookie)
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
    parser.parse_products("ботинки из натуральной кожи", 1)