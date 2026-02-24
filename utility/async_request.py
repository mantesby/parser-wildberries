import asyncio
import aiohttp
import logging
import dotenv
import os
import time
from utility.base_http import BaseHttpConifig

class AsyncWildBerriesRequest(BaseHttpConifig):
    def __init__(self, ab_testing: str = "false", appType: int = 1, curr: str = "rub",
                 dest: int = -1257786, hide_vflags: int = 4294967296, lang: str = "ru", resultset: str = "catalog",
                 sort: str = "popular", spp: int = 30, suppressSpellcheck: str = "false") -> None:
        super().__init__(ab_testing, appType, curr, dest, hide_vflags, lang, resultset, sort, spp, suppressSpellcheck)
        
        self.__session = aiohttp.ClientSession
        
    async def _fetch_page(self, page, count):
        url_card = self._url_card_info(page['id'])
        urls_image = self._url_card_images(page['id'], page["pics"])
        
        async with self.__session(cookies=self._cookie) as session:
            try:
                async with session.get(url_card, cookies=self._cookie) as response:
                    response.raise_for_status()
                    card_json = await response.json()
            except aiohttp.ClientResponseError as e:
                self.logger.error(f"HTTP error: страница карточки {url_card} Код ошибки: {e.status}, Причина: {e.message}")
            
            self.logger.info(f"Карточка {count} успешно взята")
            return {"page_info": page, "card_info": card_json, "images_info": urls_image}            
        
    async def session_page(self, query, page):
        self._params["page"] = page
        self._params["query"] = query
        
        async with self.__session(cookies=self._cookie) as session:
            tasks = []
            self.logger.debug("Получение информации для парсинга всей страницы")
            async with session.get(self._url, params=self._params, headers={"Accept": "application/json"}) as response:
                pages_json = await response.json(content_type=None)
            
            count = 0
            for page_json in pages_json["products"]:
                count += 1
                tasks.append(asyncio.create_task(self._fetch_page(page_json, count)))
            
            self.logger.debug("Задачи успешно сформированы")
            
            start_time = time.perf_counter()
            result = await asyncio.gather(*tasks)
            end_time = time.perf_counter()
            self.logger.info(f"Время выполнения: {round(end_time - start_time)} секунд")
            return result
            
    async def _get_pages_query(self, query):
        self._params["query"] = query
        self._params["page"] = 1
        self.logger.info("Извлечение количества страниц поискового запроса")
        async with self.__session(cookies=self._cookie) as session:
            async with session.get(self._url, params=self._params) as response:
                json = await response.json(content_type=None)
                return json["total"] 
            
async def main():
    dotenv.load_dotenv()
    parser = AsyncWildBerriesRequest()
    parser.set_cookie(os.getenv("X_WBAAS_TOKEN"))
    await parser.session_page("пально из натуральной кожи", 1)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())