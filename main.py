from utility.parse import WildBerriesParser
from utility.convert import write_full_info

if __name__ == "__main__":
    parser = WildBerriesParser()
    parser.set_cookie("")
    data = parser.parse_products()
    write_full_info(data)