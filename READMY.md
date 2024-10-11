# Как JSON-ответ используется веб-страницей

 Веб-страница обычно связана с бэкендом через API. Фронтенд обращается к API бэкенда с запросом на получение данных,
 на что бэкенд отвечает JSON-ответом. Затем фронтенд подставляет значения из JSON-ответа на веб-страницу, чтобы
 пользователь мог увидеть их на экране.

 В данном случае бэкенд предоставляет JSON-ответ с данными о расходах за месяц, среднем размере транзакции, сумме
 кешбэка, топе-3 категорий расходов и топе-3 транзакций. Фронтенд использует этот ответ, чтобы отобразить
 соответствующие значения на веб-странице.

 Также в данном случае бэкенд может использовать сторонние API для получения текущих цен на валюты и акции S&P500.
 Фронтенд может использовать эти данные, чтобы отобразить соответствующие значения на веб-странице.

 Реализуйте набор функций и главную функцию, принимающую на вход строку
 с датой и временем в формате YYYY-MM-DD HH:MM:SS
 и возвращающую JSON-ответ со следующими данными:
     1. Приветствие в формате "???", где ???
     — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
     в зависимости от текущего времени.
     2. По каждой карте:
         последние 4 цифры карты;
         общая сумма расходов;
         кешбэк (1 рубль на каждые 100 рублей).
     3. Топ-5 транзакций по сумме платежа.
     4. Курс валют.
     5. Стоимость акций из S&P500.

{'Дата операции': '31.12.2021 16:44:00', 'Дата платежа': '31.12.2021', 'Номер карты': '*7197', 'Статус': 'OK',
'Сумма операции': -160.89, 'Валюта операции': 'RUB', 'Сумма платежа': -160.89, 'Валюта платежа': 'RUB',
'Кэшбэк': nan, 'Категория': 'Супермаркеты', 'MCC': 5411.0, 'Описание': 'Колхоз', 'Бонусы (включая кэшбэк)': 3,
'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 160.89},

{'pagination': {'limit': 100, 'offset': 0, 'count': 42, 'total': 42}, 'data': [{'code': 'USD', 'symbol': '$', 'name': 'US Dollar'}, {'code': 'ARS', 'symbol': 'AR$', 'name': 'Argentine Peso'}, {'code': 'EUR', 'symbol': '€', 'name': 'Euro'}, {'code': 'BHD', 'symbol': 'BD', 'name': 'Bahraini Dinar'}, {'code': 'BRL', 'symbol': 'R$', 'name': 'Brazilian Real'}, {'code': 'CAD', 'symbol': 'CA$', 'name': 'Canadian Dollar'}, {'code': 'CLP', 'symbol': 'CL$', 'name': 'Chilean Peso'}, {'code': 'CNY', 'symbol': 'CN¥', 'name': 'Chinese Yuan'}, {'code': 'COP', 'symbol': 'CO$', 'name': 'Colombian Peso'}, {'code': 'DKK', 'symbol': 'Dkr', 'name': 'Danish Krone'}, {'code': 'EGP', 'symbol': 'EGP', 'name': 'Egyptian Pound'}, {'code': 'HKD', 'symbol': 'HK$', 'name': 'Hong Kong Dollar'}, {'code': 'HUF', 'symbol': 'Ft', 'name': 'Hungarian Forint'}, {'code': 'ISK', 'symbol': 'Ikr', 'name': 'Icelandic Króna'}, {'code': 'INR', 'symbol': 'Rs', 'name': 'Indian Rupee'}, {'code': 'IDR', 'symbol': 'Rp', 'name': 'Indonesian Rupiah'}, {'code': 'ILS', 'symbol': '₪', 'name': 'Israeli New Sheqel'}, {'code': 'JPY', 'symbol': '¥', 'name': 'Japanese Yen'}, {'code': 'MYR', 'symbol': 'RM', 'name': 'Malaysian Ringgit'}, {'code': 'MXN', 'symbol': 'MX$', 'name': 'Mexican Peso'}, {'code': 'NZD', 'symbol': 'NZ$', 'name': 'New Zealand Dollar'}, {'code': 'NGN', 'symbol': '₦', 'name': 'Nigerian Naira'}, {'code': 'NOK', 'symbol': 'Nkr', 'name': 'Norwegian Krone'}, {'code': 'PKR', 'symbol': 'PKRs', 'name': 'Pakistani Rupee'}, {'code': 'PEN', 'symbol': 'S/.', 'name': 'Peruvian Nuevo Sol'}, {'code': 'PHP', 'symbol': '₱', 'name': 'Philippine Peso'}, {'code': 'QAR', 'symbol': 'QR', 'name': 'Qatari Rial'}, {'code': 'RUB', 'symbol': 'RUB', 'name': 'Russian Ruble'}, {'code': 'SAR', 'symbol': 'SR', 'name': 'Saudi Riyal'}, {'code': 'SGD', 'symbol': 'S$', 'name': 'Singapore Dollar'}, {'code': 'ZAR', 'symbol': 'R', 'name': 'South African Rand'}, {'code': 'KRW', 'symbol': '₩', 'name': 'South Korean Won'}, {'code': 'CHF', 'symbol': 'CHF', 'name': 'Swiss Franc'}, {'code': 'TWD', 'symbol': 'NT$', 'name': 'New Taiwan Dollar'}, {'code': 'THB', 'symbol': '฿', 'name': 'Thai Baht'}, {'code': 'TRY', 'symbol': 'TL', 'name': 'Turkish Lira'}, {'code': 'AED', 'symbol': 'AED', 'name': 'United Arab Emirates Dirham'}, {'code': 'GBP', 'symbol': '£', 'name': 'British Pound Sterling'}, {'code': 'VND', 'symbol': '₫', 'name': 'Vietnamese Dong'}, {'code': 'AUD', 'symbol': 'A$', 'name': 'Australian Dollar'}, {'code': 'SEK', 'symbol': 'Skr', 'name': 'Swedish Krona'}, {'code': 'PLN', 'symbol': 'zł', 'name': 'Polish Zloty'}]}
 Описание данных

    Дата операции — дата, когда произошла транзакция.
    Дата платежа — дата, когда был произведен платеж.
    Номер карты — последние 4 цифры номера карты.
    Статус — статус операции (например: OK, FAILED).
    Сумма операции — сумма транзакции в оригинальной валюте.
    Валюта операции — валюта, в которой была произведена транзакция.
    Сумма платежа — сумма транзакции в валюте счета.
    Валюта платежа — валюта счета.
    Кешбэк — размер полученного кешбэка.
    Категория — категория транзакции.
    MCC — код категории транзакции (соответствует международной классификации).
    Описание — описание транзакции.
    Бонусы (включая кешбэк) — количество полученных бонусов (включая кешбэк).
    Округление на «Инвесткопилку» — сумма, которая была округлена и переведена на «Инвесткопилку».
    Сумма операции с округлением — сумма транзакции, округленная до ближайшего целого числа.
