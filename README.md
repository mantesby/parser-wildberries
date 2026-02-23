# Parser Wildberries

> Продвинутый парсер для маркетплейса wildberries.

> Разработан в качестве pet project. Которым важно анализировать рынок 

![Python Status](https://img.shields.io/badge/Python-3.13.1-blue)
![requests required](https://img.shields.io/badge/Requests-required-white)
![requests required](https://img.shields.io/badge/pandas-required-yellow)
![requests required](https://img.shields.io/badge/excel-xlsx-green)


## Инструкция
Выполните команду 
```cmd
pip install -r requirements.txt
```

В файле main.py установите собственный cookie под названием **x_wbaas_token** на сайте wildberries.
Запустите main.py
```bash
python main.py
```

## Cкорость
### Синхронный подход
1. **147** sec.
2. **152** sec.
3. **186** sec.
4. **168** sec.
5. **170** sec.


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
- [ ] Асинхронные http запросы карточкам
- [ ] Логирование
- [ ] Код ревью 