import logging


class Filter():
    def _url_card(self, card_id: int):
        return f"https://www.wildberries.ru/catalog/{card_id}/detail.aspx"
    
    def _url_seller(self, seller_id):
        return f"https://www.wildberries.ru/seller/{seller_id}"
        
    def filtered_data(self, cards):
        logger = logging.getLogger("filter")
        data_filter = []
        for card in cards:
            try:
                url_product = self._url_card(card["page_info"]["id"])
                page_seller = self._url_seller(card["page_info"]["supplierId"])
                price = card["page_info"]["sizes"][0]["price"]["product"] // 100,
                
                data = {
                    "url_card": url_product,
                    "articule": card["page_info"],
                    "name": card["page_info"]["name"],
                    "reviewRating": card["page_info"]["reviewRating"],
                    "reviews": card["page_info"]["feedbacks"],
                    "price": price,
                    "seller": card["page_info"]["brand"],
                    "page_seller": page_seller,
                    "total": card["page_info"]["totalQuantity"]
                    }
                data_filter.append(data)
            except Exception as e:
                logger.error(f"Ошибка фильтра, некоторые важные данные отсутсвуют в карточке.\
                             Она не будет включена в таблицу\nОшибка: {e}")
        return data_filter        