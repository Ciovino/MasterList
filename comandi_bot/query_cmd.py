# Comando /query
from bot_wrapper import BotWrapper
from user_info import UserInfo

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

async def execute(the_bot:BotWrapper, user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    choises = [
        [InlineKeyboardButton("amen", callback_data = 'AMEN')],
        [InlineKeyboardButton("amen-ino", callback_data = 'AMEN-INO')],
        [InlineKeyboardButton("amen-one", callback_data = 'BESTEMMIA')]
    ]

    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Scegli bro",
        reply_markup = InlineKeyboardMarkup(choises)
    )