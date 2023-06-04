import psycopg2

hostname = 'localhost'
database = 'test'
username = 'postgres'
pwd = ''
port_id = 5432

conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)

conn.close()
# ip install -Iv psycopg2-binary==2.8.4

db_host = 'localhost'
db_port = 5432
db_name = 'test'
db_user = 'postgres'
db_password = '123'

# Токен доступа к телеграм-боту
bot_token = ''

# Создание подключения к базе данных
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password
)

cursor = conn.cursor()
cursor.execute('SELECT * FROM test')
result = cursor.fetchall()
cursor.close()

for row in result:
    print(row)

# Создание экземпляра телеграм-бота
bot = telebot.TeleBot(bot_token)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Привет! Я бот, подключенный к базе данных PostgreSQL! Я могу вывести информацию о игроке по его ID (/playerinfo), представления (/views), хранимые процедуры (/procedures) или добавить нового игрока в таблицу(/addplayer).")

    @bot.message_handler(commands=['views'])
    def handle_start(message):
        bot.reply_to(message, "Я могу вывести представления о командах из дивизионов Atlantic (/Atlantic), Pacific (/Pacific) и Metropolitan (/Metropolitan).")

    # Пример запроса к базе данных
        @bot.message_handler(commands=['Atlantic'])
        def handle_get_data(message):
            try:
                # Создание объекта курсора
                cursor = conn.cursor()

                # Выполнение запроса к базе данных
                cursor.execute('SELECT * FROM atl')
                result = cursor.fetchall()

                cursor.close()

                formatted_result = ''
                for row in result:
                    formatted_row = ', '.join(str(value) for value in row)
                    formatted_result += f"- {formatted_row}\n"

                # Отправка форматированного вывода пользователю
                if formatted_result:
                    bot.reply_to(message, f"Перечень команд дивизиона Atlantic:\n{formatted_result}")
                else:
                    bot.reply_to(message, "Представление пустое.")
            except Exception as e:
                bot.reply_to(message, "An error occurred while fetching data.")

        @bot.message_handler(commands=['Pacific'])
        def handle_get_data(message):
            try:
                # Создание объекта курсора
                cursor = conn.cursor()

                # Выполнение запроса к базе данных
                cursor.execute('SELECT * FROM pac')
                result = cursor.fetchall()

                cursor.close()

                formatted_result = ''
                for row in result:
                    formatted_row = ', '.join(str(value) for value in row)
                    formatted_result += f"- {formatted_row}\n"

                # Отправка форматированного вывода пользователю
                if formatted_result:
                    bot.reply_to(message, f"Перечень команд дивизиона Pacific:\n{formatted_result}")
                else:
                    bot.reply_to(message, "Представление пустое.")
            except Exception as e:
                bot.reply_to(message, "An error occurred while fetching data.")

        @bot.message_handler(commands=['Metropolitan'])
        def handle_get_data(message):
            try:
                # Создание объекта курсора
                cursor = conn.cursor()

                # Выполнение запроса к базе данных
                cursor.execute('SELECT * FROM metr')
                result = cursor.fetchall()

                cursor.close()

                formatted_result = ''
                for row in result:
                    formatted_row = ', '.join(str(value) for value in row)
                    formatted_result += f"- {formatted_row}\n"

                # Отправка форматированного вывода пользователю
                if formatted_result:
                    bot.reply_to(message, f"Перечень команд дивизиона Metropolitan:\n{formatted_result}")
                else:
                    bot.reply_to(message, "Представление пустое.")
            except Exception as e:
                bot.reply_to(message, "An error occurred while fetching data.")


    @bot.message_handler(commands=['procedures'])
    def handle_start(message):
        bot.reply_to(message, "Я могу вывести хранимые процедуры: вместимость всех стадионов Канады(/Canadaarena) и количество игроков, вес которых больше или равен числу введенному пользователем(/playerwght). Также можно с помощью процедуры изменять вес игроков по ID(/update_weight)")

        @bot.message_handler(commands=['update_weight'])
        def handle_update_weight(message):
            try:
                # Запрашиваем у пользователя идентификатор игрока
                bot.reply_to(message, "Введите идентификатор игрока:")

                @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
                def handle_player_id_input(message):
                    try:
                        player_id = int(message.text)

                        # Запрашиваем у пользователя новый вес
                        bot.reply_to(message, "Введите новый вес игрока:")

                        @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
                        def handle_weight_input(message):
                            try:
                                weight = int(message.text)

                                # Создание объекта курсора
                                cursor = conn.cursor()

                                # Вызов хранимой процедуры для обновления веса игрока
                                procedure_name = 'update_player_weight'
                                cursor.execute(f"CALL {procedure_name}({player_id}, {weight})")

                                # Применение изменений в базе данных
                                conn.commit()

                                cursor.close()

                                bot.reply_to(message, "Вес игрока успешно обновлен.")
                            except ValueError:
                                bot.reply_to(message, "Некорректный ввод веса.")

                            except Exception as e:
                                bot.reply_to(message, "Произошла ошибка при обновлении данных.")

                        bot.register_next_step_handler(message, handle_weight_input)

                    except ValueError:
                        bot.reply_to(message, "Некорректный идентификатор игрока.")

                    except Exception as e:
                        bot.reply_to(message, "Произошла ошибка при обновлении данных.")
                bot.register_next_step_handler(message, handle_player_id_input)

            except Exception as e:
                bot.reply_to(message, "Произошла ошибка при обновлении данных.")

        @bot.message_handler(commands=['Canadaarena'])
        def handle_get_data(message):
            try:
                # Создание объекта курсора
                cursor = conn.cursor()

                # Вызов хранимой процедуры
                procedure_name = 'get_capacitycanada_sum1'
                cursor.execute("CALL get_capacitycanada_sum1(NULL)")

                # Получение результата процедуры
                result = cursor.fetchone()

                cursor.close()

                # Отправка результата пользователю
                if result is not None:
                    result_string = str(result)[1:-1]  # Удаление первой и последней скобки
                    result_string = result_string.replace(',', '')  # Удаление запятых
                    bot.reply_to(message, result_string)
                else:
                    bot.reply_to(message, "No data found.")
            except Exception as e:
                bot.reply_to(message, "An error occurred while fetching data.")


        @bot.message_handler(commands=['playerwght'])
        def handle_get_data(message):
            try:
                # Запрашиваем у пользователя ввод веса
                bot.reply_to(message, "Введите вес:")

                @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
                def handle_weight_input(message):
                    try:
                        weight = int(message.text)

                        # Создание объекта курсора
                        cursor = conn.cursor()

                        # Вызов хранимой процедуры
                        procedure_name = 'get_playerwght_count'
                        cursor.execute(f"CALL get_playerwght_count({weight}, NULL)")

                        # Получение результата процедуры
                        result = cursor.fetchone()

                        cursor.close()

                        # Отправка результата пользователю
                        if result is not None:
                            result_string = str(result)[1:-1]  # Удаление первой и последней скобки
                            result_string = result_string.replace(',', '')  # Удаление запятых
                            bot.reply_to(message, result_string)
                        else:
                            bot.reply_to(message, "Данные не найдены.")
                    except ValueError:
                        bot.reply_to(message, "Некорректный ввод веса.")
                    except Exception as e:
                        bot.reply_to(message, "Произошла ошибка при получении данных.")
            except Exception as e:
                bot.reply_to(message, "Произошла ошибка при получении данных.")
            # Обработчик команды /addplayer


    @bot.message_handler(commands=['addplayer'])
    def handle_add_player(message):
        try:
            # Запрашиваем у пользователя ввод информации о новом игроке
            bot.reply_to(message,
                         "Введите информацию о новом игроке в формате: \nID игрока, \nИмя, \nДата рождения(в формате гггг-мм-дд), \nГород рождения, \nАмплуа, \nРост, \nВес, \nID команды, \nЗарплата, \nУчастие в национальной сборной")

            @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
            def handle_player_info_input(message):
                try:
                    player_info = message.text.split(', ')
                    pid = int(player_info[0])
                    name = player_info[1]
                    birth = player_info[2]
                    city = player_info[3]
                    role = player_info[4]
                    height = int(player_info[5])
                    weight = int(player_info[6])
                    teamid = int(player_info[7])
                    salary = int(player_info[8])
                    part = player_info[9]

                    # Создание объекта курсора
                    cursor = conn.cursor()

                    # Выполнение INSERT-запроса для добавления нового игрока
                    cursor.execute(
                        f"INSERT INTO player (id_player, player_name, day_of_birth, city_of_birth, player_role, height, weight, id_team, salary, participation_in_national_team) VALUES ('{pid}', '{name}','{birth}','{city}','{role}','{height}','{weight}','{teamid}','{salary}','{part}')")
                    conn.commit()

                    cursor.close()

                    bot.reply_to(message, "Новый игрок успешно добавлен в базу данных.")
                except ValueError:
                    bot.reply_to(message, "Некорректный ввод информации о новом игроке.")
                except Exception as e:
                    bot.reply_to(message, "Произошла ошибка при добавлении игрока в базу данных.")
                return
        except Exception as e:
            bot.reply_to(message, "Произошла ошибка при добавлении игрока в базу данных.")

    # Обработчик команды /playerinfo
    @bot.message_handler(commands=['playerinfo'])
    def handle_player_info(message):
        try:
            # Запрашиваем у пользователя ввод ID игрока
            bot.reply_to(message, "Введите ID игрока:")

            @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
            def handle_player_id_input(message):
                try:
                    player_id = int(message.text)

                    # Создание объекта курсора
                    cursor = conn.cursor()

                    # Выполнение запроса к базе данных для получения информации об игроке
                    cursor.execute(f"SELECT * FROM player WHERE id_player = {player_id}")
                    result = cursor.fetchone()

                    cursor.close()

                    if result:
                        # Форматирование информации об игроке
                        player_info = f"ID: {result[0]}\nИмя: {result[1]}\nДата рождения: {result[2]}\nГород рождения: {result[3]}\nАмплуа: {result[4]}\nРост: {result[5]}\nВес: {result[6]}\nID команды: {result[7]}\nЗарплата: {result[8]}\nУчастие в национальной сборной: {result[9]}"

                        # Отправка информации об игроке пользователю
                        bot.reply_to(message, player_info)

                    else:
                        bot.reply_to(message, "Игрок с указанным ID не найден.")
                except ValueError:
                    bot.reply_to(message, "Некорректный ввод ID игрока.")
                except Exception as e:
                    bot.reply_to(message, "Произошла ошибка при получении информации об игроке.")
                finally:
                    return  # Return to the start function

        except Exception as e:
            bot.reply_to(message, "Произошла ошибка при получении информации об игроке.")



# Запуск телеграм-бота
bot.polling()

# Закрытие соединения с базой данных
conn.close() #1