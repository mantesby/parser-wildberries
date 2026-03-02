# Parser Wildberries

> Продвинутый парсер для маркетплейса wildberries.

> Разработан в качестве pet project.

![Python Status](https://img.shields.io/badge/Python-3.13.1-blue)
![requests required](https://img.shields.io/badge/Requests-required-white)
![pandas required](https://img.shields.io/badge/pandas-required-yellow)
![aiohttp required](https://img.shields.io/badge/aiohttp-required-violet)
![excel required](https://img.shields.io/badge/excel-xlsx-green)


## Инструкция
Выполните команду 
```cmd
pip install git+https://github.com/mantesby/parser-wildberries
```

В файле main.py установите собственный cookie под названием **x_wbaas_token**, его можно достать при заходе на сайт wildberries.
Запустите main.py
```bash
python main.py
```

## Cкорость
### Асинхронный подход
1. **4** sec.
2. **4** sec.
3. **7** sec.
4. **2** sec.
5. **5** sec.

## TODO
### Parse
- [x] Артикул
- [x] Название
- [x] Ссылка на товар
- [x] Цена
- [x] Описание
- [x] Ссылка на изображение
- [x] Все характеристики
- [x] Название селлера
- [x] Ссылка селлера
- [x] Размеры товара через запятую
- [x] Остатки по товару (число)
- [x] Рейтинг
- [x] Количество отзывов
### Data storage
- [x] Сохранение данных в xlsx файл
- [x] Отдельный файл xlsx для рейтинга, стоимости и страны
### Roadmap (опционально)
- [x] Асинхронные http запросы карточкам
- [x] Логирование
- [x] Код ревью 
