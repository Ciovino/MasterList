# Comando /start
from bot_wrapper import BotWrapper
from user_info import UserInfo

from telegram import Update
from telegram.ext import ContextTypes

async def execute(the_bot:BotWrapper, user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = the_bot.return_mex("saluto", user, update.message)    
    
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = text,
        parse_mode = 'MarkdownV2'
    )

    user.change_state('in_ascolto')