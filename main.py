import dotenv
import os
import asyncio
from utility.async_parse import AsyncWildberriesParser


async def main():
    dotenv.load_dotenv()
    parser = AsyncWildberriesParser()
    parser.set_cookie(os.getenv("X_WBAAS_TOKEN"))
    await parser.start()


if __name__ == "__main__":
    asyncio.run(main())
