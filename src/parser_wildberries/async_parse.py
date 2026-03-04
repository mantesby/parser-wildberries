from parser_wildberries.async_http.async_request import AsyncWildBerriesRequest
from parser_wildberries.file_saver import XlsxManager
from parser_wildberries.filter import Filter


class AsyncWildberriesParser(AsyncWildBerriesRequest, Filter, XlsxManager):
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

    async def start(self) -> None:
        DEFAULT_QUERY = "пальто из натуральной шерсти"
        QUERY_INPUT_TEXT = f"Введите поисковый запрос (по умолчанию '{DEFAULT_QUERY}'):"
        query = input(QUERY_INPUT_TEXT) or DEFAULT_QUERY

        len_cards = await self._get_pages_query(query)
        pages = len_cards // 100 + 1
        description_card = f"Введите страницу для парсинга от 1 до {pages}"
        page = int(input(f"{description_card} (всего {len_cards} карточек): "))
        json_data = await self.session_page(query, page)
        filter_data = self.filtered_data(json_data)
        self.save_to_excel(filter_data, "parser_wb.xlsx", "parser_wb_filter.xlsx")
