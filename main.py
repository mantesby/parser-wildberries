import asyncio
import logging
from os import getenv

from parser_wildberries import AsyncWildberriesParser


async def main():
    logging.basicConfig(level=logging.INFO)
    parser = AsyncWildberriesParser()
    parser.set_cookie(getenv("X_WBAAS_TOKEN"))
    await parser.start()


if __name__ == "__main__":
    asyncio.run(main())
