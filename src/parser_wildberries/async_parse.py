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
        query = (
            input(
                "Введите поисковый запрос (по умолчанию 'пальто из натуральной шубы'): "
            )
            or "пальто из натуральной шерсти"
        )
        len_cards = await self._get_pages_query(query)
        pages = len_cards // 100 + 1
        page = int(
            input(
                f"""Введите страницу которую вы хотите спарсить от 1 до {pages}
                (всего {len_cards} карточек): """
            )
        )
        json_data = await self.session_page(query, page)
        filter_data = self.filtered_data(json_data)
        self.save_to_excel(filter_data)
