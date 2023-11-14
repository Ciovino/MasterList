from secret_stuff import bot_token
from user_info import UserInfo
from bot_wrapper import BotWrapper

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from comandi_bot import state_cmd, back_cmd, start_cmd, pappagallo_cmd, count_cmd, query_cmd

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

list_bot = BotWrapper('bot\\known_users.json', 'bot\\bot_mex.json')

async def main_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = list_bot.is_known_user(update.effective_user.id)
    if user == None:
        user = list_bot.add_user(UserInfo(update.effective_user.id, update.effective_user.full_name, []))

    command = update.message.text.split(' ')[0].removeprefix('/')

    if not user.is_valid_command(command):
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "comando non valido"
        )
        return
    
    if not user.change_state(command):
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "impossibile cambiare stato"
        )
        return

    if command == 'back':
        await back_cmd.execute(list_bot, user, update, context)
        return

    if command == 'start':
        await start_cmd.execute(list_bot, user, update, context)
        return

    if command == 'state':
        await state_cmd.execute(list_bot, user, update, context)
        return
    
    if command == 'pappagallo':
        await pappagallo_cmd.execute(list_bot, user, update, context)
        return
    
    if command == 'count':
        await count_cmd.execute(list_bot, user, update, context)
        return
    
    if command == 'query':
        await query_cmd.execute(list_bot, user, update, context)
        return

async def normal_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = list_bot.is_known_user(update.effective_user.id)
    if user == None:
        user = list_bot.add_user(UserInfo(update.effective_user.id, update.effective_user.full_name, []))
    
    if not user.is_mex_state():
        return

    state = user.get_current_state()

    if state == 'pappagallo':
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = list_bot.return_mex("echo", user, update.message)
        )
        return

    if state == 'count':
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f'{len(update.message.text.split(" "))}'
        )
        return

async def callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = list_bot.is_known_user(update.effective_user.id)
    if user == None:
        user = list_bot.add_user(UserInfo(update.effective_user.id, update.effective_user.full_name, []))

    if not user.is_query_state():
        return

    query = update.callback_query

    await query.answer()
    await query.delete_message()

    state = user.get_current_state()
    
    if state == 'query':
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = query.data
        )

    await query_cmd.execute(list_bot, user, update, context)

if __name__ == '__main__':
    # Crea il bot
    application = ApplicationBuilder().token(bot_token).build()

    # Comandi
    main_command_handler = MessageHandler(filters.COMMAND, main_command)
    application.add_handler(main_command_handler)

    # Messaggi normali
    normal_message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), normal_message)
    application.add_handler(normal_message_handler)

    # Callback query
    callback_query_handler = CallbackQueryHandler(callback_query)
    application.add_handler(callback_query_handler)

    # Avvia il bot
    application.run_polling()