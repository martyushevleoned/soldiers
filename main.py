# pip install PyTelegramBotAPI
import telebot
import config
import func

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['text'])
def send_text(m):
    # print(config.registred_user)
    # Проверка регистрации
    if m.chat.id in config.registred_user.keys():

        print(config.command)

        for i in config.command:
            if config.registred_user[m.chat.id] == i[0]:
                if i[1] in config.registred_user.values():
                    bot.send_message(func.get_key(i[1]), func.get_surname(i[0]) + ':\n' + m.text, reply_markup=None)
                    bot.send_message(m.chat.id, 'Приказ доведён до подчинённого', reply_markup=None)
                else:
                    i.append(m.text)
                    config.later.append(i)
                    bot.send_message(m.chat.id, 'Приказ доводится до подчинённого', reply_markup=None)

                config.command.pop(config.command.index(i))

        bot.send_message(m.chat.id, 'Меню:', reply_markup=config.menu_key)
    else:
        # Проверяем правильность логина и пароля
        if func.registration(m):
            bot.send_message(m.chat.id, 'Вход успешно выполнен:', reply_markup=config.menu_key)
            func.later_msg(bot)
        else:
            bot.send_message(m.chat.id, 'Введите логин и пароль')


@bot.callback_query_handler(func=lambda call: True)
def handler_call(call):
    if call.message.chat.id not in config.registred_user.keys():
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='Вы были лишены прав',
            reply_markup=None)

    elif call.data == 'private':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=func.get_private(call.message.chat.id),
            reply_markup=config.back_key)

    elif call.data == 'personnel':
        text, key = func.get_personnel(config.registred_user[call.message.chat.id],
                                       config.registred_user[call.message.chat.id])
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=key)

    elif call.data == 'exit':
        if call.message.chat.id in config.registred_user.keys():
            config.registred_user.pop(call.message.chat.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='До свидания',
            reply_markup=None)

    elif call.data == 'home':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='меню:',
            reply_markup=config.menu_key)

    elif 'sol' in call.data:
        flag, solider_id = eval(call.data)
        config.command.append([config.registred_user[call.message.chat.id], solider_id])
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='Напишите содержание приказа для: ' + func.get_surname(solider_id),
            reply_markup=None)

    elif 'un' in call.data:
        flag, solider_id = eval(call.data)
        text, key = func.get_personnel(config.registred_user[call.message.chat.id], solider_id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=key)


bot.polling(none_stop=True)
