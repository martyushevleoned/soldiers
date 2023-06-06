from telebot import types

TOKEN = '5217065698:AAHneltVnqgSTma9IylFZ4yjCyZR6en-EIA'

HOSTNAME = 'localhost'
DATABASE = 'military'
USERNAME = 'postgres'
PWD = '123'
PORT_ID = 5432

query = {
    '/who_am_i': 'who_am_i',  # Уставное обращение к военнослужащему
    '/buildings': 'buildings',  # Строения воинских частях
    '/speciality': 'speciality',  # Специальности военнослужащих в округе
    '/property': 'property'  # Имущество подразделений
}

# user_id
# id_военнослужащего
registred_user = {}

# логин
# пароль
# id_военнослужащего
users = [['', '7збъ', 149],  # Командир военного округа

         ['', 'я9г3', 62],  # Командир ВЧ----1
         ['', 'шрвс', 61],  # Командир Р---1
         ['', '7пч9', 17],  # Командир В-1
         ['', 'сяжв', 25],  # Командир В-2
         ['', '9щу1', 45],  # Командир В-3
         ['', 'вфвй', 63],  # Командир Р---2
         ['', 'хьпф', 64],  # Командир В-1
         ['', 'рцёя', 65],  # Командир В-2
         ['', 'ндх7', 66],  # Командир В-3

         ['', 'яр2с', 122],  # Командир ВЧ----2
         ['', '40н9', 123],  # Командир Р---1
         ['', 'жшхн', 125],  # Командир В-1
         ['', 'ия1ы', 126],  # Командир В-2
         ['', 'о033', 127],  # Командир В-3
         ['', 'е52н', 124],  # Командир Р---2
         ['', 'лхаы', 128],  # Командир В-1
         ['', 'кк7е', 129],  # Командир В-2
         ['', 'вы1ё', 130],  # Командир В-3

         ['', 'юд82', 4],  # ВЧ1 Р1 В1 О1
         ['', '53ер', 238],  # ВЧ2 Р2 В3 О3
         ['', '4усл', 115],  # ВЧ1 Р2 В3 О2
         ['', 'оягб', 186],  # ВЧ2 Р1 В3 О2

         ['', 'оягб', 1],
         ['', 'оягб', 2],
         ['', 'оягб', 3],

         ]

# это флаг для отдачи приказа
# кто отдаёт
# кому отдаёт
command = []

# кто
# кому
# что
later = []

# клавиатуры
menu_key = types.InlineKeyboardMarkup()
menu_key.add(types.InlineKeyboardButton(text='Личное дело', callback_data='private'))
menu_key.add(types.InlineKeyboardButton(text='Личный состав', callback_data='personnel'))
menu_key.add(types.InlineKeyboardButton(text='Выход', callback_data='exit'))

back_key = types.InlineKeyboardMarkup()
back_key.add(types.InlineKeyboardButton(text='Назад', callback_data='home'))
