import logging


class Filter:
    def _url_card(self, card_id: int):
        return f"https://www.wildberries.ru/catalog/{card_id}/detail.aspx"

    def _url_seller(self, seller_id):
        return f"https://www.wildberries.ru/seller/{seller_id}"

    def _sizes(self, sizes):
        sizes = []
        for size in sizes:
            sizes.append(size["name"])
        return sizes

    def filtered_data(self, cards):
        logger = logging.getLogger("filter")
        data_filter = []
        for card in cards:
            try:
                url_product = self._url_card(card["page_info"]["id"])
                page_seller = self._url_seller(card["page_info"]["supplierId"])
                price = card["page_info"]["sizes"][0]["price"]["product"] // 100
                sizes = self._sizes(card["page_info"]["sizes"])
                info = card["card_info"]["grouped_options"]

                data = {
                    "url_card": url_product,
                    "articule": card["page_info"]["id"],
                    "name": card["page_info"]["name"],
                    "reviewRating": card["page_info"]["reviewRating"],
                    "reviews": card["page_info"]["feedbacks"],
                    "price": price,
                    "seller": card["page_info"]["brand"],
                    "page_seller": page_seller,
                    "total": card["page_info"]["totalQuantity"],
                    "sizes": sizes,
                    "description": card["card_info"]["description"],
                    "main_info": info[0],
                    "additional_info": info[1],
                    "pics": card["images_info"],
                }
                data_filter.append(data)
                logger.debug(
                    f"Данные карточки с артикулом {data['articule']} отфильтрованы"
                )
            except Exception as e:
                logger.error(
                    f"Ошибка в карточке {card['page_info']['id']}: отсутствует поле {e}"
                )
        logger.info("Данные успешно отфильтрованы")
        return data_filter
