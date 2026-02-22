import csv
import parse

parser = parse.WildBerriesParser()
parser.set_cookie("1.1000.7c6a2931091a4657a8a5138016d80c99.MTV8NjYuMTUxLjQwLjQzfE1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xNDQuMC4wLjAgU2FmYXJpLzUzNy4zNnwxNzcyNzk1NTE4fHJldXNhYmxlfDJ8ZXlKb1lYTm9Jam9pSW4wPXwwfDN8MTc3MjE5MDcxOHwx.MEYCIQCaQh2KDTChuOCWHVu5LZ1OVINtcqkAayhU3EisU9uoHQIhAOqLbQy8LBfy9GiUDRKiek1xP6gFvNvBoVhkXOosTUEn")

cards = parser.parse_products("ботинки из натуральной кожи", 1)

with open('parser_wildberries.csv', 'w', newline='', encoding="utf-8-sig") as csvfile:
    fieldnames = ['Ссылка на товар', 'Артикул', "Название", "Цена", "Описание",
                  "Ссылки на изображения", "Основная информация", "Дополнительная информация",
                  "Название селлера", "Ссылка на селлера", "Размеры товара",
                  "Остатки товара", "Рейтинг", "Количество отзывов"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for card in cards:
        urls_pics = ""
        for pic in card["pics"]:
            urls_pics += f"{pic},"
        
        main_text = ""
        for main_field in card["main_info"]["options"]:
            main_text = f"{main_field['name']}: {main_field["value"]},"
            
        additional_text = ""
        for additional_field in card["additional_info"]["options"]:
            additional_field = f"{additional_field['name']}: {additional_field["value"]},"
        
        size_text = ""
        for size in card["size"]:
            size_text = f"{size},"
            
        writer.writerow({"Ссылка на товар": card['url_card'], "Артикул": card["id"],
                         "Название": card["name"], "Цена": card["price"],
                         "Описание": card["description"], "Ссылки на изображения": urls_pics,
                         "Основная информация": main_text, "Дополнительная информация": additional_text,
                         "Название селлера": card["seller"], "Ссылка на селлера": card["page_seller"],
                         "Размеры товара": size_text, "Остатки товара": card["total"],
                         "Рейтинг": card["reviewRating"], "Количество отзывов": card["reviews"]})