# pip install psycopg2
import psycopg2
import config
from telebot import types

conn = psycopg2.connect(
    host=config.HOSTNAME,
    dbname=config.DATABASE,
    user=config.USERNAME,
    password=config.PWD,
    port=config.PORT_ID
)


# Проверка есть ли юзер в базе
def registration(m):
    for i in config.users:
        if i[0] in m.text and i[1] in m.text:
            # сопоставляем user_id и id_военнослужащего
            config.registred_user[m.chat.id] = i[2]
            return True
    return False


# Возвращает всю информацию о военнослужащем по id_военнослужащего
# причём на вход принимает user_id
def get_private(user_id):
    cursor = conn.cursor()
    cursor.execute(f'select * from get_private({config.registred_user[user_id]})')
    result = cursor.fetchall()[0]
    cursor.close()
    text = f'ФИО:  {result[3]}\n' + \
           f'Звание:  {result[4]}\n' + \
           f'Состав:  {result[5]}\n' + \
           f'Должность:  {result[6]}\n' + \
           f'Специальность:  {result[7]}\n' + \
           f'Выслуга лет:  {result[8]}\n'
    return text


# Чисто чтоб обращаться в формате <Звание> <Фамилия>
# Принимает id_военнослужащего
def get_surname(user_id):
    cursor = conn.cursor()
    cursor.execute(f'select * from get_private({user_id})')
    result = cursor.fetchall()[0]
    cursor.close()
    text = f'{result[4]} {result[3]}'
    return text


# эт пздц
# проверка на то является ли пользователь командиром
# если нет то так и пишем
# если да то
# 1) пишем для кого он является непосредственным начальником
# 2) генерируем клавиатуру в callback_data которой проносим флаг
# это дерьмо необходимо пояснить
# если командир нажал на военнослужащего то через callback_data в main проносится флаг "sol" и id_военнослужащего
# если командир нажал на подразделение то через callback_data в main проносится флаг "un" и id_командира_подразделения
#
# на вход принимает:
# id военнослужащего
# id командира подразделения чей личный состав мы хотим посмотреть
def get_personnel(sol_id, commander_id):
    # Первая логическая часть
    # Просто делаем запрос чтоб правильно назвать кем является пользователь
    cursor = conn.cursor()
    cursor.execute(f'select * from who_am_i where "ID_военнослужащего" = {sol_id}')
    result = cursor.fetchall()
    cursor.close()

    # У обычных работяг нет подчинённых подразделений поэтому нет и строк в результате запроса
    if len(result) == 0:
        return 'нет подчинённых', config.back_key

    # командиром какого подразделения он является sol_id
    # print(f'id подразделения {result[0][2]}')
    text = f'Вы {result[0][1]}: {result[0][2]}\n'

    # В чём тут фишка
    # командир должен иметь возможность обратиться ко всем своим подчинённым
    # допустим командир роты (sol_id) хочет обратиться к подчинённым командира взвода (commander_id)
    # этого мы смотрим есть ли в подчинении подразделения
    # если нет то подразделение является отделением и нам достаточно просто вывести список отделения
    # если в подчинении есть подразделения
    cursor = conn.cursor()
    cursor.execute(
        f'select * from Военнослужащий '
        f'inner join Подразделение '
        f'on Военнослужащий."ID_подчинённого_подразделения" = Подразделение."ID_подразделения" '
        f'where Военнослужащий."ID_военнослужащего" = {commander_id}')
    result = cursor.fetchall()
    cursor.close()

    # командиром какого подразделения он является
    # print(f'id подразделения {result[0][2]}')
    text += f'Вы обращаетесь к {result[0][11]}: {result[0][15]}\n'
    text += 'Выберите кому отдать приказ:'

    # список подчинённыx подразделений
    cursor = conn.cursor()
    cursor.execute(f'select * from get_personnel({result[0][2]})')
    union = cursor.fetchall()
    cursor.close()

    # начинаем генерировать главу
    key = types.InlineKeyboardMarkup()

    # Если нет подчинённых подразделений то выводим список личного состава
    if len(union) == 0:
        cursor = conn.cursor()
        cursor.execute(f'select * from Военнослужащий where "ID_подразделения" = {result[0][2]}')
        soldier = cursor.fetchall()
        cursor.close()

        for s in soldier:
            print(s)
            if s[0] != commander_id:
                key.add(types.InlineKeyboardButton(text=s[4] + ' ' + s[3], callback_data='\'sol\',' + str(s[0])))
        print()
    else:
        # Выводим список должностных лиц подразделения и инфу о самом подразделении
        for u in union:
            cursor = conn.cursor()
            cursor.execute(f'select * from get_private({u[0]})')
            soldier = cursor.fetchall()
            cursor.close()

            print(u)
            key.add(types.InlineKeyboardButton(text=u[2] + ': ' + u[6], callback_data='\'un\',' + str(u[0])))

            for s in soldier:
                print(s)
                key.add(types.InlineKeyboardButton(text=s[6] + ': ' + s[4] + ' ' + s[3],
                                                   callback_data='\'sol\',' + str(s[0])))
    print()

    key.add(types.InlineKeyboardButton(text='Назад', callback_data='home'))

    return text, key


# id пользоватаеля из id военнослужащего
def get_key(val):
    for k, v in config.registred_user.items():
        if v == val:
            return k


def later_msg(bot):
    arr = []
    for i in config.later:
        if get_key(i[1]) in config.registred_user:
            bot.send_message(get_key(i[1]), get_surname(i[0]) + ':\n' + i[2], reply_markup=None)
            arr.append(i)
    for i in arr:
        config.later.pop(config.later.index(i))


def set_register(sol_id, text_type, text):

    print(f'call set_register({sol_id}, \'{text_type}\', \'{text}\')')
    #
    # cursor = conn.cursor()
    # cursor.execute(f'SET search_path TO military; call set_register({sol_id} ::integer, \'{str(text_type)}\' ::text, \'{str(text)}\' ::text)')
    # conn.commit()
    # cursor.close()
