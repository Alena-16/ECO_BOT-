# ЭКО_бот
## Обработчик команды /start
<img width="666" height="177" alt="start" src="https://github.com/user-attachments/assets/1c7463fd-1673-444e-9d8f-405fdadd7aef" />\
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я бот ECO_ALENAbot! Напиши /help, чтобы узнать что я умею')
    
## Обработчик команды /help 
<img width="407" height="188" alt="image" src="https://github.com/user-attachments/assets/43127275-d42f-456d-b116-95da07874abf" />\
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, напиши /ECO_sovet, чтобы узнать экологичные советы; напиши /rubbish, чтобы узнать куда правильно сдавать мусор; напиши /eco_action, чтобы поучаствовать в акциях; напиши /ECOnom, чтобы получить советы, по экономии природных ресурсов; напиши /ECOcompetition, чтобы поучаствовать в конкурсе, помочь нашей планете и в конце года получить приз.") 

## Обработчик команды /ECO_sovet
<img width="395" height="147" alt="2025-09-27_23-11-14" src="https://github.com/user-attachments/assets/ec40b2da-07bd-4b31-a370-7f687f7993e1" />\
def gen_sovet():
    soveti = ["Сдайте батарейки и лампочки в пункт переработки", "устройте день без автомобиля", "используйте бумажные пакеты вместо пластиковых", "посадите дерево"]
    return random.choice(soveti)
@bot.message_handler(commands=['ECO_sovet'])
def vernut_sovet(message):
    back_sovet = gen_sovet()
    bot.reply_to(message, back_sovet) 

## Обработчик команды /rubbish
<img width="352" height="102" alt="image" src="https://github.com/user-attachments/assets/ba2e65d5-3fce-4e60-be91-424e6b0a5db9" />\
def gen_fact():
    facti = ["бумагу помещайте в синие контейнеры", "пищевые отходы помещайте в коричневые контейнеры", "пластик помещайте в оранжевые контейнеры", "стекло помещайте в зелёные контейнеры", "металл сдавайте в специальные пункты приёма"]
    return random.choice(facti)
@bot.message_handler(commands=['rubbish'])
def vernut_fact(message):
    back_fact = gen_fact()
    bot.reply_to(message, back_fact)

## Обработчик команды /eco_action
<img width="408" height="222" alt="image" src="https://github.com/user-attachments/assets/d9dab672-085a-4c51-bb1c-a278e8578ca9" />\
@bot.message_handler(commands=['eco_action'])
def vernut_ssilky(message):
    bot.reply_to(message, "https://ecowiki.ru/ - это ссылка на сайт, где можно узнать о местах проведения экологических акций 🌏😘")

## Обработчик команды /ECOnom
<img width="413" height="277" alt="image" src="https://github.com/user-attachments/assets/4bc5d8ab-95ea-4898-a120-ab16633207b1" />\
@bot.message_handler(commands=['ECOnom'])
def vernut_econom_sovet(message):
    econom_back_sovet = gen_econom_sovet()
    bot.reply_to(message, econom_back_sovet)

## Обработчик команды /ECOcompetition
<img width="408" height="282" alt="image" src="https://github.com/user-attachments/assets/b86d8175-9786-4367-9b39-89659c3e99d3" />\
@bot.message_handler(commands=['ECOcompetition'])
def send_rules(message):
    bot.reply_to(message, "Участвуя в ECO-конкурсе, будешь получать баллы. Расценка баллов:\n 1 Сдал пластик в переработку (код /plastic) – 2 балла \n 2 Сдал батарейку в переработку (код /battery) – 5 баллов \n 3 В течение дня перемещался без автомобиля (код /on_foot) – 4 балла \n 4 Сортировал мусор (код /sort)  – 4 балла \n 5 Придумал вторую жизнь старой вещи (код /re_use) – 6 баллов \n 6 Поучаствовал в эко-акции (код /ECO_action) – 5 баллов \n 7 Привел друга в эко-движение(код /ECO_friend) – 10 баллов \n Хочешь посмотреть рейтинг ( код /table) \n Чтобы получить баллы, кликни на код ECO-доброго дела из перечисленных выше.")

## Обработчик команды /table
<img width="411" height="295" alt="table" src="https://github.com/user-attachments/assets/35ce2993-9121-454a-a725-f0699819de84" />\
@bot.message_handler(commands=['table'])
def ad_table(message):
    tg_id = message.from_user.id
    username = message.from_user.username

    # сначала добавляем пользователя, если его ещё нет
    db.add_sub(tg_id)

    # достаём текущее количество сданного пластика
    conn = db._connect()
    cur = conn.cursor()
    cur.execute("SELECT re_plast, score FROM users WHERE tg_id=?", (tg_id,))
    row = cur.fetchone()
    conn.close()

    current_plast = int(row["re_plast"]) if row["re_plast"] else 0
    current_score = int(row["score"]) if row["score"] else 0

    # добавляем 2 к количеству баллов за пластик и +2 балла к общему счету
    new_plast = current_plast + 0
    new_score = current_score + 0
    print(tg_id)

    db.add_col("re_plast", tg_id, str(new_plast))
    db.add_col("score", tg_id, str(new_score))

    conn =  db._connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY CAST(score as INTEGER) DESC")
    rows = cur.fetchall()
    conn.close()
    place = next((i+1 for i, row in  enumerate(rows) if row["tg_id"] == tg_id), None)
    headers = rows[0].keys() if row else []
    table = ", таблица лидеров:\n\n"
    table += " | ".join(headers) + "\n"
    table += "-" * 50 + "\n"
    for i, row in enumerate(rows, start=1):
        values = [str(row[h]) if row[h] is not None else "-" for h in headers]
        table += f"{i}. " + " | ".join(values) + "\n"

    bot.reply_to(message, f"твоё место в реинтинге {place}"
                 f"{table}\n\n"
                 f"/help \n\n"
                 f"/ECOcompetition, /plastic, /battery, /on_foot, /sort, /re_use, /ECO_action, /ECO_friend, /table")

## Обработчик команд /plastik, battery, on_foot, sort, /re_use, /ECO_action, /ECO_friend
### рассмотрим на примере /plastik
<img width="620" height="528" alt="2025-09-27_23-56-25" src="https://github.com/user-attachments/assets/37bc2ab1-1689-4329-b1dc-2a1bf7cf9ce3" />\
@bot.message_handler(commands=['plastic'])
def add_plastic(message):
    tg_id = message.from_user.id
    username = message.from_user.username

    # сначала добавляем пользователя, если его ещё нет
    db.add_sub(tg_id)

    # достаём текущее количество сданного пластика
    conn = db._connect()
    cur = conn.cursor()
    cur.execute("SELECT re_plast, score FROM users WHERE tg_id=?", (tg_id,))
    row = cur.fetchone()
    conn.close()

    current_plast = int(row["re_plast"]) if row["re_plast"] else 0
    current_score = int(row["score"]) if row["score"] else 0

    # добавляем 2 к количеству баллов за пластик и +2 балла к общему счету
    new_plast = current_plast + 2 
    new_score = current_score + 2
    db.add_col("re_plast", tg_id, str(new_plast))
    db.add_col("score", tg_id, str(new_score))

    conn =  db._connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY CAST(score as INTEGER) DESC")
    rows = cur.fetchall()
    conn.close()
    place = next((i+1 for i, row in  enumerate(rows) if row["tg_id"] == tg_id), None)
    headers = rows[0].keys() if row else []
    table = ", таблица лидеров:\n\n"
    table += " | ".join(headers) + "\n"
    table += "-" * 50 + "\n"
    for i, row in enumerate(rows, start=1):
        values = [str(row[h]) if row[h] is not None else "-" for h in headers]
        table += f"{i}. " + " | ".join(values) + "\n"

    bot.reply_to(message, f"Ты сдал пластик \n"
                 f"твое кол-во баллов за сдачу пластика: {new_plast} и общее количество баллов: {new_score}  \n\n"
                 f"твоё место в реинтинге {place}"
                 f"{table}\n\n"
                 f"/help \n\n"
                 f"/ECOcompetition, /plastic, /battery, /on_foot, /sort, /re_use, /ECO_action, /ECO_friend, /table")
