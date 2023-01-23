# Домашнее задание по теме "Веб-скрапинг"

В Python проекте, используется фреймворк scrapy для извлечения информации о ноутбуках с веб-сайтов.
Собираемые данные складываются в таблицу `db.sqlite3`, в следующем формате:

| Столбец | Тип данных | Описание |
| ------- | ---------- | -------- |
| id | int | | 
| link | varchar | ссылка на страницу товара |
| timestamp | timestamp | время посещения страницы |
| title | varchar | наименование товара |
| freq_i | float | частота процессора, ГГц |
| ram | int | объем ОЗУ, Гб |
| rom | int | оъем ПЗУ, Гб |
| price | int | цена, руб |
| rank | float | вычисляемый рейтинг |

Вычисление рейтинга выполняется по формуле:

$$ rank=\sum_{i=1}^nX_i*W_i $$

_где:_
* _X -- параметр техники (например объем оперативной памяти);_
* _W -- вес этого отдельно взятого параметра (определяется индивидуально по каждому параметру);_
* _n -- количество параметров._

При вычислении рейтинга испоьзовались веса:
| ram | вес |
| --- | --- |
| $$ 4 \leqslant ram < 8 $$ | 4.6 |
| $$ 8 \leqslant ram  < 12 $$ | 5.6 |
| $$ 12 \leqslant ram  < 16 $$ | 6.6 |
| $$ 32 \leqslant ram  < 32 $$ | 7.6 |
| $$ ram \geqslant 32 $$ | 8.6 |

## Как установить
```sh
$ git clone https://github.com/polipych/hw_13.git
$ pip install -r requirements.txt
```

## Как запустить
```sh
$ py .\main.py
```

## ТОП-5
id	link	timestamp	title	freq_i	ram	rom	price	rank
684	https://www.notik.ru/goods/notebooks-msi-titan-gt77-12uhs-208ru-black-91471.htm	2023-01-23 11:15:57.737008	MSI Titan GT77 12UHS-208RU i9-12900HX	2.3	64	3072	426600	406.16
384	https://www.notik.ru/goods/notebooks-msi-stealth-gs77-12uhs-030ru-black-91481.htm	2023-01-23 11:15:43.377461	MSI Stealth GS77 12UHS-030RU i9-12900H	2.5	64	2048	338900	406.12
683	https://www.notik.ru/goods/notebooks-msi-stealth-gs66-12uhs-267ru-black-91489.htm	2023-01-23 11:15:57.729028	MSI Stealth GS66 12UHS-267RU i9-12900H	2.5	64	2048	341600	405.85
385	https://www.notik.ru/goods/notebooks-msi-creator-z17-a12uhst-258ru-gray-92333.htm	2023-01-23 11:15:43.382447	MSI Creator Z17 A12UHST-258RU i9-12900H	2.5	64	2048	359900	404.02
267	https://www.notik.ru/goods/notebooks-msi-creatorpro-z16p-b12umst-223ru-gray-91967.htm	2023-01-23 11:15:35.481945	MSI CreatorPro Z16P B12UMST-223RU i9-12900H	2.5	64	2048	369900	403.02
