import logging


class BaseHttpConifig:
    def __init__(
        self,
        ab_testing: str = "false",
        appType: int = 1,
        curr: str = "rub",
        dest: int = -1257786,
        hide_vflags: int = 4294967296,
        lang: str = "ru",
        resultset: str = "catalog",
        sort: str = "popular",
        spp: int = 30,
        suppressSpellcheck: str = "false",
    ) -> None:
        """

        Attributes:
            ab_testing: Сравнение двух вариантов элемента карточки товара, лучше всегда false.
            appType: Тип приложения: 1 = веб, 4 = мобильное. Влияет на формат данных.
            curr: rub - рубли, usd - доллары и т.д.
            dest: Регион или склад. Определяет наличие товара и цену.
            hide_vflags: Не знаю. Лучше не трогать.
            lang: Язык интерфейса и описаний товаров.
            resultset: Скорее всего тип поиска. Обычно catalog.
            sort: Сортировка результатов: популярные, по цене, рейтингу и т.д.
            spp: Количество товаров на одной странице.

        """

        self._url = "https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search"
        self.logger = logging.getLogger("request")

        self._cookie = {"x_wbaas_token": ""}
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
            "suppressSpellcheck": suppressSpellcheck,
        }

    def set_cookie(self, cookie):
        self._cookie["x_wbaas_token"] = cookie

    def _url_card_base(self, card_id: int) -> str:
        vol = card_id // 100000
        part = card_id // 1000
        shard = self._get_basket(vol)
        self.logger.debug("Использование базового url для id {card_id}")
        return f"https://basket-{shard}.wbbasket.ru/vol{vol}/part{part}/{card_id}"

    def _url_card_info(self, card_id: int) -> str:
        base_url = self._url_card_base(card_id)
        self.logger.debug("Карточка основной информации с id {card_id}")
        return f"{base_url}/info/ru/card.json"

    def _url_card_images(self, card_id: int, length_pic: int) -> list[str]:
        base_url = self._url_card_base(card_id)
        urls_image = []
        for number_pic in range(1, length_pic + 1):
            urls_image.append(base_url + f"images/big/{number_pic}.webp")
        self.logger.debug(
            "urls изображений товара с id {card_id}, а их количество {length_pic}"
        )
        return urls_image

    def _get_basket(self, vol: int) -> str:
        self.logger.debug("Поиск шардов товара")
        if vol <= 143:
            return "01"
        elif vol >= 144 and vol <= 287:
            return "02"
        elif vol >= 288 and vol <= 431:
            return "03"
        elif vol >= 432 and vol <= 719:
            return "04"
        elif vol >= 720 and vol <= 1007:
            return "05"
        elif vol >= 1008 and vol <= 1061:
            return "06"
        elif vol >= 1062 and vol <= 1115:
            return "07"
        elif vol >= 1116 and vol <= 1169:
            return "08"
        elif vol >= 1170 and vol <= 1313:
            return "09"
        elif vol >= 1314 and vol <= 1601:
            return "10"
        elif vol >= 1602 and vol <= 1655:
            return "11"
        elif vol >= 1656 and vol <= 1919:
            return "12"
        elif vol >= 1920 and vol <= 2045:
            return "13"
        elif vol >= 2046 and vol <= 2189:
            return "14"
        elif vol >= 2190 and vol <= 2405:
            return "15"
        elif vol >= 2406 and vol <= 2621:
            return "16"
        elif vol >= 2622 and vol <= 2837:
            return "17"
        elif vol >= 2838 and vol <= 3053:
            return "18"
        elif vol >= 3054 and vol <= 3269:
            return "19"
        elif vol >= 3270 and vol <= 3485:
            return "20"
        elif vol >= 3486 and vol <= 3701:
            return "21"
        elif vol >= 3702 and vol <= 3917:
            return "22"
        elif vol >= 3918 and vol <= 4133:
            return "23"
        elif vol >= 4134 and vol <= 4349:
            return "24"
        elif vol >= 4350 and vol <= 4555:
            return "25"
        elif vol >= 4566 and vol <= 4877:
            return "26"
        elif vol >= 4878 and vol <= 5189:
            return "27"
        elif vol >= 5190 and vol <= 5501:
            return "28"
        elif vol >= 5502 and vol <= 5813:
            return "29"
        elif vol >= 5814 and vol <= 6125:
            return "30"
        elif vol >= 6126 and vol <= 6437:
            return "31"
        elif vol >= 6438 and vol <= 6749:
            return "32"
        elif vol >= 6750 and vol <= 7061:
            return "33"
        elif vol >= 7062 and vol <= 7373:
            return "34"
        elif vol >= 7374 and vol <= 7685:
            return "35"
        elif vol >= 7686 and vol <= 7997:
            return "36"
        elif vol >= 7998 and vol <= 8309:
            return "37"
        elif vol >= 8310 and vol <= 8621:
            return "38"
        elif vol >= 8622 and vol <= 8933:
            return "39"
        elif vol >= 8934 and vol <= 9245:
            return "40"
        else:
            return "41"
