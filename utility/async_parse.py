import requests
import json
import asyncio
import aiohttp

class AsyncWildBerriesParser():
    
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
        
    async def session(self):
        pass