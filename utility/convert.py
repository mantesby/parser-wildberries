import csv
import pandas as pd
import os

def write_full_info(cards: list):
    with open('parser_wildberries.csv', 'a', newline='', encoding="utf-8-sig") as csvfile:
        fieldnames = ['Ссылка на товар', 'Артикул', "Название", "Цена", "Описание",
                    "Ссылки на изображения", "Основная информация", "Дополнительная информация",
                    "Название селлера", "Ссылка на селлера", "Размеры товара",
                    "Остатки товара", "Рейтинг", "Количество отзывов"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for card in cards:
            urls_pics = ""
            for pic in card["pics"]:
                urls_pics += f"{pic},"
            
            main_text = ""
            for main_field in card["main_info"]["options"]:
                main_text = f"{main_field['name']}: {main_field["value"]},"
                
            additional_text = ""
            country = ""
            for additional_field in card["additional_info"]["options"]:
                additional_text = f"{additional_field['name']}: {additional_field["value"]},"
                if additional_field['name'] == "Страна производства":
                    country = additional_field['value']
                    
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
            
            if card["reviewRating"] >= 4.5 and card["price"] <= 10000 and country == "Россия":
                with open('parser_wildberries_filter.csv', 'a', newline='', encoding="utf-8-sig") as csv_filterfile:
                    fieldnames = ['Ссылка на товар', 'Артикул', "Название", "Цена", "Описание",
                        "Ссылки на изображения", "Основная информация", "Дополнительная информация",
                        "Название селлера", "Ссылка на селлера", "Размеры товара",
                        "Остатки товара", "Рейтинг", "Количество отзывов"]
                    
                    writer_filter = csv.DictWriter(csv_filterfile, fieldnames=fieldnames)
                    writer_filter.writerow({"Ссылка на товар": card['url_card'], "Артикул": card["id"],
                            "Название": card["name"], "Цена": card["price"],
                            "Описание": card["description"], "Ссылки на изображения": urls_pics,
                            "Основная информация": main_text, "Дополнительная информация": additional_text,
                            "Название селлера": card["seller"], "Ссылка на селлера": card["page_seller"],
                            "Размеры товара": size_text, "Остатки товара": card["total"],
                            "Рейтинг": card["reviewRating"], "Количество отзывов": card["reviews"]})
    df = pd.read_csv("parser_wildberries.csv")
    df.to_excel("wb.xlsx")
    df_filter = pd.read_csv('parser_wildberries_filter.csv')
    df_filter.to_excel("wb_filter.xlsx")

