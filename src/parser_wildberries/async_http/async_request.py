import asyncio
import time

import aiohttp

from parser_wildberries.async_http.base_http import BaseHttpConifig


class AsyncWildBerriesRequest(BaseHttpConifig):
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
        super().__init__(
            ab_testing,
            appType,
            curr,
            dest,
            hide_vflags,
            lang,
            resultset,
            sort,
            spp,
            suppressSpellcheck,
        )

        self.__session = aiohttp.ClientSession

    async def _fetch_page(self, page, count):
        url_card = self._url_card_info(page["id"])
        urls_image = self._url_card_images(page["id"], page["pics"])
        card_json = ""

        async with self.__session(cookies=self._cookie) as session:
            try:
                async with session.get(url_card, cookies=self._cookie) as response:
                    response.raise_for_status()
                    card_json = await response.json()
            except aiohttp.ClientResponseError as e:
                self.logger.error(
                    f"""HTTP error: page card: {url_card}.
                    code error: {e.status}.
                    reason: {e.message}"""
                )

            self.logger.info(f"Card {count} have parsed successful")
            return {
                "page_info": page,
                "card_info": card_json,
                "images_info": urls_image,
            }

    async def session_page(self, query, page):
        self._params["page"] = page
        self._params["query"] = query

        async with self.__session(cookies=self._cookie) as session:
            tasks = []
            self.logger.debug("Get info for parsing all page")
            async with session.get(
                self._url, params=self._params, headers={"Accept": "application/json"}
            ) as response:
                pages_json = await response.json(content_type=None)

            count = 0
            for page_json in pages_json["products"]:
                count += 1
                tasks.append(asyncio.create_task(self._fetch_page(page_json, count)))

            self.logger.debug("Tasks created successful")

            start_time = time.perf_counter()
            result = await asyncio.gather(*tasks)
            end_time = time.perf_counter()
            self.logger.info(f"Execution time: {round(end_time - start_time)} sec.")
            return result

    async def _get_pages_query(self, query):
        self._params["query"] = query
        self._params["page"] = 1
        self.logger.info("Extracting the number of pages of a search query")
        async with self.__session(cookies=self._cookie) as session:
            async with session.get(self._url, params=self._params) as response:
                json = await response.json(content_type=None)
                return json["total"]
