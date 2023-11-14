# Comando /count
from bot_wrapper import BotWrapper
from user_info import UserInfo

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

async def execute(the_bot:BotWrapper, user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "conteggio tattico",
        parse_mode = 'MarkdownV2'
    )