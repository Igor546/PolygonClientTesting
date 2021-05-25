# PolygonClientTesting

### Тестовое задание
 
 1. Подключиться к API сервиса: https://polygon.io/
    `Выполненно используя "RESTClient"`
 2. Необходимо настроить выгрузку из сервиса через запрос к нему – минутные бары:
    `Реализована выгрузка как минутных так и 5min/15min/30min/60min/240min`
    Символы для выгрузки: MSFT, COST, EBAY, WMT, GOOGL
 3. Cоздать простой веб интерфейс, его функционал:
    - выпадающий список символов                                                                                                           
    - при выборе символа, отображение свечного графика символа (подгрузка данных через API с сервиса https://polygon.io/  и обновление их в БД)
    `График отрисовывается с использованием библиотеки "matplotlib". Так же мной была реализована прокрутка графика.`                                                                                                                      
    - выбор периода данных для отображения данных на графике
 4. Хранение данных на локальной БД (PostgreSQL, либо БД, с которой есть большой опыт работы)
    `Для хранения данных использую JSON формат и базу данных "MongoDB"`
 
### Итог работы

![alt tag](https://i.imgur.com/fSbSn9u.png "Главное окно программы")
