import bisect
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
            ab_testing: Сравнение двух вариантов элемента карточки товара.
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
        self.logger.debug("Search shards")
        vol_shards = [
            143,
            287,
            431,
            719,
            1007,
            1061,
            1115,
            1169,
            1313,
            1601,
            1655,
            1919,
            2045,
            2189,
            2405,
            2621,
            2837,
            3053,
            3269,
            3485,
            3701,
            3917,
            4133,
            4349,
            4555,
            4877,
            5189,
            5501,
            5813,
            6125,
            6437,
            6749,
            7061,
            7373,
            7685,
            7997,
            8309,
            8621,
            8933,
            9245,
            9557,
        ]

        integer_shard = bisect.bisect_left(vol_shards, vol) + 1
        if integer_shard <= 9:
            return f"0{integer_shard}"
        return str(integer_shard)
