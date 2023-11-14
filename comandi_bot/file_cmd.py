# Comando /file
from bot_wrapper import BotWrapper
from user_info import UserInfo

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def execute(the_bot:BotWrapper, user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline_keyboard = [
        [InlineKeyboardButton(the_bot.return_mex("file_cmd_1", user, update.message), callback_data='new_file')],
        [InlineKeyboardButton(the_bot.return_mex("file_cmd_2", user, update.message), callback_data='change_active')],
        [InlineKeyboardButton(the_bot.return_mex("file_cmd_3", user, update.message), callback_data='save_file')],
        [InlineKeyboardButton(the_bot.return_mex("file_cmd_4", user, update.message), callback_data='delete_file')]
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=the_bot.return_mex("file_cmd_0", user, update.message),
        reply_markup=InlineKeyboardMarkup(inline_keyboard), 
        parse_mode='MarkdownV2'
    )