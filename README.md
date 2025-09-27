# ЭКО_бот
## Обработчик команды /start
<img width="666" height="177" alt="start" src="https://github.com/user-attachments/assets/1c7463fd-1673-444e-9d8f-405fdadd7aef" />
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я бот ECO_ALENAbot! Напиши /help, чтобы узнать что я умею')
    
## Обработчик команды /help 
<img width="407" height="188" alt="image" src="https://github.com/user-attachments/assets/43127275-d42f-456d-b116-95da07874abf" /> 
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, напиши /ECO_sovet, чтобы узнать экологичные советы; напиши /rubbish, чтобы узнать куда правильно сдавать мусор; напиши /eco_action, чтобы поучаствовать в акциях; напиши /ECOnom, чтобы получить советы, по экономии природных ресурсов; напиши /ECOcompetition, чтобы поучаствовать в конкурсе, помочь нашей планете и в конце года получить приз.") 

## Обработчик команды /ECO_sovet
<img width="395" height="147" alt="2025-09-27_23-11-14" src="https://github.com/user-attachments/assets/ec40b2da-07bd-4b31-a370-7f687f7993e1" />
def gen_sovet():
    soveti = ["Сдайте батарейки и лампочки в пункт переработки", "устройте день без автомобиля", "используйте бумажные пакеты вместо пластиковых", "посадите дерево"]
    return random.choice(soveti)
@bot.message_handler(commands=['ECO_sovet'])
def vernut_sovet(message):
    back_sovet = gen_sovet()
    bot.reply_to(message, back_sovet) 

## Обработчик команды /rubbish
<img width="352" height="102" alt="image" src="https://github.com/user-attachments/assets/ba2e65d5-3fce-4e60-be91-424e6b0a5db9" />
def gen_fact():
    facti = ["бумагу помещайте в синие контейнеры", "пищевые отходы помещайте в коричневые контейнеры", "пластик помещайте в оранжевые контейнеры", "стекло помещайте в зелёные контейнеры", "металл сдавайте в специальные пункты приёма"]
    return random.choice(facti)
@bot.message_handler(commands=['rubbish'])
def vernut_fact(message):
    back_fact = gen_fact()
    bot.reply_to(message, back_fact)
