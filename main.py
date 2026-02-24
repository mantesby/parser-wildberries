import dotenv
import os
import asyncio
from utility.async_request import AsyncWildBerriesRequest
from utility.filter import Filter

async def main():
    dotenv.load_dotenv()
    parser = AsyncWildBerriesRequest()
    parser.set_cookie(os.getenv("X_WBAAS_TOKEN"))
    data = await parser.session_page("пальто из натуральной шерсти", 1)
    convert = Filter()
    convert.filtered_data(data)
    
if __name__ == "__main__":
    asyncio.run(main())