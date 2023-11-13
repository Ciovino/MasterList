# Comando /back
from user_info import UserInfo
from bot_wrapper import BotWrapper

from telegram import Update
from telegram.ext import ContextTypes

async def execute(the_bot:BotWrapper, user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text = the_bot.return_mex("back", user, update.message),
        parse_mode="Markdownv2"
    )

    user.change_state('in_ascolto')