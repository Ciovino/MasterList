# Comando /state
from bot_wrapper import BotWrapper
from user_info import UserInfo

from telegram import Update
from telegram.ext import ContextTypes

async def execute(the_bot:BotWrapper, user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    user.change_state(user.get_previous_state())

    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = the_bot.return_mex("state", user, update.message)
    )