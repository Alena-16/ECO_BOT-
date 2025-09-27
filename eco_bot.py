import telebot
import os
import requests
import random
bot = telebot.TeleBot("7679444233:AAGaY6Lhg_R6B3ygVt41OciX1NVxmLdxNvk")

import db   # добавляем в начале eco_bot.py
# def get_leadboard():
#     conn =  db._connect()
#     cur = conn.cursor()
#     cur.execute("SELECT tg_id, username, re_plast, ")
# Обработчик команды '/start' и '/hello'
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я бот ECO_ALENAbot! Напиши /help, чтобы узнать что я умею')

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, напиши /ECO_sovet, чтобы узнать экологичные советы; напиши /rubbish, чтобы узнать куда правильно сдавать мусор; напиши /eco_action, чтобы поучаствовать в акциях; напиши /ECOnom, чтобы получить советы, по экономии природных ресурсов; напиши /ECOcompetition, чтобы поучаствовать в конкурсе, помочь нашей планете и в конце года получить приз.")

def gen_sovet():
    soveti = ["Сдайте батарейки и лампочки в пункт переработки", "устройте день без автомобиля", "используйте бумажные пакеты вместо пластиковых", "посадите дерево"]
    return random.choice(soveti)

@bot.message_handler(commands=['ECO_sovet'])
def vernut_sovet(message):
    back_sovet = gen_sovet()
    bot.reply_to(message, back_sovet)

def gen_fact():
    facti = ["бумагу помещайте в синие контейнеры", "пищевые отходы помещайте в коричневые контейнеры", "пластик помещайте в оранжевые контейнеры", "стекло помещайте в зелёные контейнеры", "металл сдавайте в специальные пункты приёма"]
    return random.choice(facti)

@bot.message_handler(commands=['rubbish'])
def vernut_fact(message):
    back_fact = gen_fact()
    bot.reply_to(message, back_fact)

@bot.message_handler(commands=['eco_action'])
def vernut_ssilky(message):
    bot.reply_to(message, "https://ecowiki.ru/ - это ссылка на сайт, где можно узнать о местах проведения экологических акций 🌏😘")

def gen_econom_sovet():
    e_soveti = ["не включайте свет, когда светло", "закрывайте кран, когда вам не нужна вода", "полностью наполняйте стиральную машину", "используйте многоразовую посуду", "ходите в магазин с многоразовой сумкой", "замените обычные лампы на энергосберегающие", "выключайте из разетки всю неиспользуемую бытовую технику", "при использовании бытовой техники пользуйтесь программами экономичных режимов", "поставьте холодильник подальше от тепла и чаще мойте уплотнитель на его двери", "отремонтируйте сантехнику"]
    return random.choice(e_soveti)

@bot.message_handler(commands=['ECOnom'])
def vernut_econom_sovet(message):
    econom_back_sovet = gen_econom_sovet()
    bot.reply_to(message, econom_back_sovet)


@bot.message_handler(commands=['ECOcompetition'])
def send_rules(message):
    bot.reply_to(message, "Участвуя в ECO-конкурсе, будешь получать баллы. Расценка баллов:\n 1 Сдал пластик в переработку (код /plastic) – 2 балла \n 2 Сдал батарейку в переработку (код /battery) – 5 баллов \n 3 В течение дня перемещался без автомобиля (код /on_foot) – 4 балла \n 4 Сортировал мусор (код /sort)  – 4 балла \n 5 Придумал вторую жизнь старой вещи (код /re_use) – 6 баллов \n 6 Поучаствовал в эко-акции (код /ECO_action) – 5 баллов \n 7 Привел друга в эко-движение(код /ECO_friend) – 10 баллов \n Хочешь посмотреть рейтинг ( код /table) \n Чтобы получить баллы, кликни на код ECO-доброго дела из перечисленных выше.")

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
#______________________________________________________________________________________________________________________
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
    
   
  

@bot.message_handler(commands=['battery'])
def add_battery(message):
    tg_id = message.from_user.id
    username = message.from_user.username

    # сначала добавляем пользователя, если его ещё нет
    db.add_sub(tg_id)

    # достаём текущее количество сданных батареек и общий счёт
    conn = db._connect()
    cur = conn.cursor()
    cur.execute("SELECT re_battery, score FROM users WHERE tg_id=?", (tg_id,))
    row = cur.fetchone()
    conn.close()

    current_battery = int(row["re_battery"]) if row["re_battery"] else 0
    current_score = int(row["score"]) if row["score"] else 0

    # добавляем 5 к количеству баллов за батарейки и +5 баллов к общему счету
    new_battery = current_battery + 5
    new_score = current_score + 5
    db.add_col("re_battery", tg_id, str(new_battery))
    db.add_col("score", tg_id, str(new_score))

    conn = db._connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY CAST(score as INTEGER) DESC")
    rows = cur.fetchall()
    conn.close()

    place = next((i+1 for i, row in enumerate(rows) if row["tg_id"] == tg_id), None)
    headers = rows[0].keys() if row else []
    table = ", таблица лидеров:\n\n"
    table += " | ".join(headers) + "\n"
    table += "-" * 50 + "\n"
    for i, row in enumerate(rows, start=1):
        values = [str(row[h]) if row[h] is not None else "-" for h in headers]
        table += f"{i}. " + " | ".join(values) + "\n"

    bot.reply_to(message, f"Ты сдал батарейки \n"
                 f"твое кол-во баллов за сдачу батареек: {new_battery} и общее количество баллов: {new_score}  \n\n"
                 f"твоё место в реинтинге {place}"
                 f"{table}\n\n"
                 f"/help \n\n"
                 f"/ECOcompetition, /plastic, /battery, /on_foot, /sort, /re_use, /ECO_action, /ECO_friend, /table")

@bot.message_handler(commands=['on_foot'])
def add_foot(message):
    tg_id = message.from_user.id
    username = message.from_user.username

    # сначала добавляем пользователя, если его ещё нет
    db.add_sub(tg_id)

    # достаём текущее количество сданных батареек и общий счёт
    conn = db._connect()
    cur = conn.cursor()
    cur.execute("SELECT on_foot, score FROM users WHERE tg_id=?", (tg_id,))
    row = cur.fetchone()
    conn.close()

    current_foot = int(row["on_foot"]) if row["on_foot"] else 0
    current_score = int(row["score"]) if row["score"] else 0

    # добавляем 5 к количеству баллов за батарейки и +5 баллов к общему счету
    new_foot = current_foot + 4
    new_score = current_score + 4
    db.add_col("on_foot", tg_id, str(new_foot))
    db.add_col("score", tg_id, str(new_score))

    conn = db._connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY CAST(score as INTEGER) DESC")
    rows = cur.fetchall()
    conn.close()

    place = next((i+1 for i, row in enumerate(rows) if row["tg_id"] == tg_id), None)
    headers = rows[0].keys() if row else []
    table = ", таблица лидеров:\n\n"
    table += " | ".join(headers) + "\n"
    table += "-" * 50 + "\n"
    for i, row in enumerate(rows, start=1):
        values = [str(row[h]) if row[h] is not None else "-" for h in headers]
        table += f"{i}. " + " | ".join(values) + "\n"

    bot.reply_to(message, f"Ты проехал не на автомобиле \n"
                 f"твое кол-во баллов за проезд не на аавтомобиле: {new_foot} и общее количество баллов: {new_score}  \n\n"
                 f"твоё место в реинтинге {place}"
                 f"{table}\n\n"
                 f"/help \n\n"
                 f"/ECOcompetition, /plastic, /battery, /on_foot, /sort, /re_use, /ECO_action, /ECO_friend, /table")

@bot.message_handler(commands=['sort'])
def add_sort(message):
    tg_id = message.from_user.id
    username = message.from_user.username

    # сначала добавляем пользователя, если его ещё нет
    db.add_sub(tg_id)

    # достаём текущее количество сданных батареек и общий счёт
    conn = db._connect()
    cur = conn.cursor()
    cur.execute("SELECT sort, score FROM users WHERE tg_id=?", (tg_id,))
    row = cur.fetchone()
    conn.close()

    current_sort = int(row["sort"]) if row["sort"] else 0
    current_score = int(row["score"]) if row["score"] else 0

    # добавляем 5 к количеству баллов за батарейки и +5 баллов к общему счету
    new_sort = current_sort + 4
    new_score = current_score + 4
    db.add_col("sort", tg_id, str(new_sort))
    db.add_col("score", tg_id, str(new_score))

    conn = db._connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY CAST(score as INTEGER) DESC")
    rows = cur.fetchall()
    conn.close()

    place = next((i+1 for i, row in enumerate(rows) if row["tg_id"] == tg_id), None)
    headers = rows[0].keys() if row else []
    table = ", таблица лидеров:\n\n"
    table += " | ".join(headers) + "\n"
    table += "-" * 50 + "\n"
    for i, row in enumerate(rows, start=1):
        values = [str(row[h]) if row[h] is not None else "-" for h in headers]
        table += f"{i}. " + " | ".join(values) + "\n"

    bot.reply_to(message, f"Ты сортировал мусор \n"
                 f"твое кол-во баллов за сортировку мусора: {new_sort} и общее количество баллов: {new_score}  \n\n"
                 f"твоё место в реинтинге {place}"
                 f"{table}\n\n"
                 f"/help \n\n"
                 f"/ECOcompetition, /plastic, /battery, /on_foot, /sort, /re_use, /ECO_action, /ECO_friend, /table")
    
@bot.message_handler(commands=['re_use'])
def add_use(message):
    tg_id = message.from_user.id
    username = message.from_user.username

    # сначала добавляем пользователя, если его ещё нет
    db.add_sub(tg_id)

    # достаём текущее количество сданных батареек и общий счёт
    conn = db._connect()
    cur = conn.cursor()
    cur.execute("SELECT re_use, score FROM users WHERE tg_id=?", (tg_id,))
    row = cur.fetchone()
    conn.close()

    current_use = int(row["re_use"]) if row["re_use"] else 0
    current_score = int(row["score"]) if row["score"] else 0

    # добавляем 5 к количеству баллов за батарейки и +5 баллов к общему счету
    new_use = current_use + 6
    new_score = current_score + 6
    db.add_col("re_use", tg_id, str(new_use))
    db.add_col("score", tg_id, str(new_score))

    conn = db._connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY CAST(score as INTEGER) DESC")
    rows = cur.fetchall()
    conn.close()

    place = next((i+1 for i, row in enumerate(rows) if row["tg_id"] == tg_id), None)
    headers = rows[0].keys() if row else []
    table = ", таблица лидеров:\n\n"
    table += " | ".join(headers) + "\n"
    table += "-" * 50 + "\n"
    for i, row in enumerate(rows, start=1):
        values = [str(row[h]) if row[h] is not None else "-" for h in headers]
        table += f"{i}. " + " | ".join(values) + "\n"

    bot.reply_to(message, f"Ты сдал придумал вещи вторую жизнь \n"
                 f"твое кол-во баллов за вторую жизнь вещи: {new_use} и общее количество баллов: {new_score}  \n\n"
                 f"твоё место в реинтинге {place}"
                 f"{table}\n\n"
                 f"/help \n\n"
                 f"/ECOcompetition, /plastic, /battery, /on_foot, /sort, /re_use, /ECO_action, /ECO_friend, /table")

@bot.message_handler(commands=['ECO_action'])
def add_battery(message):
    tg_id = message.from_user.id
    username = message.from_user.username

    # сначала добавляем пользователя, если его ещё нет
    db.add_sub(tg_id)

    # достаём текущее количество сданных батареек и общий счёт
    conn = db._connect()
    cur = conn.cursor()
    cur.execute("SELECT ECO_action, score FROM users WHERE tg_id=?", (tg_id,))
    row = cur.fetchone()
    conn.close()

    current_aciton = int(row["ECO_action"]) if row["ECO_action"] else 0
    current_score = int(row["score"]) if row["score"] else 0

    # добавляем 5 к количеству баллов за батарейки и +5 баллов к общему счету
    new_action = current_aciton + 5
    new_score = current_score + 5
    db.add_col("ECO_action", tg_id, str(new_action))
    db.add_col("score", tg_id, str(new_score))

    conn = db._connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY CAST(score as INTEGER) DESC")
    rows = cur.fetchall()
    conn.close()

    place = next((i+1 for i, row in enumerate(rows) if row["tg_id"] == tg_id), None)
    headers = rows[0].keys() if row else []
    table = ", таблица лидеров:\n\n"
    table += " | ".join(headers) + "\n"
    table += "-" * 50 + "\n"
    for i, row in enumerate(rows, start=1):
        values = [str(row[h]) if row[h] is not None else "-" for h in headers]
        table += f"{i}. " + " | ".join(values) + "\n"

    bot.reply_to(message, f"Ты поучаствовал в ЭКО_акции \n"
                 f"твое кол-во баллов за участие в ЭКО_акции: {new_action} и общее количество баллов: {new_score}  \n\n"
                 f"твоё место в реинтинге {place}"
                 f"{table}\n\n"
                 f"/help \n\n"
                 f"/ECOcompetition, /plastic, /battery, /on_foot, /sort, /re_use, /ECO_action, /ECO_friend, /table")

@bot.message_handler(commands=['ECO_friend'])
def add_battery(message):
    tg_id = message.from_user.id
    username = message.from_user.username

    # сначала добавляем пользователя, если его ещё нет
    db.add_sub(tg_id)

    # достаём текущее количество сданных батареек и общий счёт
    conn = db._connect()
    cur = conn.cursor()
    cur.execute("SELECT ECO_friend, score FROM users WHERE tg_id=?", (tg_id,))
    row = cur.fetchone()
    conn.close()

    current_friend = int(row["ECO_friend"]) if row["ECO_friend"] else 0
    current_score = int(row["score"]) if row["score"] else 0

    # добавляем 5 к количеству баллов за батарейки и +5 баллов к общему счету
    new_friend = current_friend + 10
    new_score = current_score + 10
    db.add_col("ECO_friend", tg_id, str(new_friend))
    db.add_col("score", tg_id, str(new_score))

    conn = db._connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY CAST(score as INTEGER) DESC")
    rows = cur.fetchall()
    conn.close()

    place = next((i+1 for i, row in enumerate(rows) if row["tg_id"] == tg_id), None)
    headers = rows[0].keys() if row else []
    table = ", таблица лидеров:\n\n"
    table += " | ".join(headers) + "\n"
    table += "-" * 50 + "\n"
    for i, row in enumerate(rows, start=1):
        values = [str(row[h]) if row[h] is not None else "-" for h in headers]
        table += f"{i}. " + " | ".join(values) + "\n"

    bot.reply_to(message, f"Ты привёл друга \n"
                 f"твое кол-во баллов за нового участника ЭКО_бота: {new_friend} и общее количество баллов: {new_score}  \n\n"
                 f"твоё место в реинтинге {place}"
                 f"{table}\n\n"
                 f"/help \n\n"
                 f"/ECOcompetition, /plastic, /battery, /on_foot, /sort, /re_use, /ECO_action, /ECO_friend, /table")

if __name__ == "__main__":
    bot.polling(none_stop=True)

bot.infinity_polling()
