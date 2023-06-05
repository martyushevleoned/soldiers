from telebot import types

TOKEN = '5217065698:AAHneltVnqgSTma9IylFZ4yjCyZR6en-EIA'

HOSTNAME = 'localhost'
DATABASE = 'military'
USERNAME = 'postgres'
PWD = '123'
PORT_ID = 5432

# user_id
# id_военнослужащего
registred_user = {}

# логин
# пароль
# id_военнослужащего
users = [['123', '123', 3],
         ['456', '456', 45],
         ['789', '789', 62]]

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
