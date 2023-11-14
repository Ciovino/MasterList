from secret_stuff import bot_token
from user_info import UserInfo
from bot_wrapper import BotWrapper

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from comandi_bot import state_cmd, back_cmd, start_cmd, pappagallo_cmd

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

async def normal_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = list_bot.is_known_user(update.effective_user.id)
    if user == None:
        user = list_bot.add_user(UserInfo(update.effective_user.id, update.effective_user.full_name, []))
    
    if user.get_current_state() == 'pappagallo':
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = list_bot.return_mex("echo", user, update.message)
        )

if __name__ == '__main__':
    # Crea il bot
    application = ApplicationBuilder().token(bot_token).build()

    # Comandi
    main_command_handler = MessageHandler(filters.COMMAND, main_command)
    application.add_handler(main_command_handler)

    # Messaggi normali
    normal_message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), normal_message)
    application.add_handler(normal_message_handler)

    # Avvia il bot
    application.run_polling()