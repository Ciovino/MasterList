# Comando /about
from secret_stuff import github_repo_url

from bot_wrapper import BotWrapper
from user_info import UserInfo

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def execute(the_bot:BotWrapper, user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline_keyboard = [
        [InlineKeyboardButton(the_bot.return_mex("about_1", user, update.message), callback_data='lista_comandi')],
        [InlineKeyboardButton(the_bot.return_mex("about_2", user, update.message), callback_data='versione')],
        [InlineKeyboardButton(the_bot.return_mex("about_3", user, update.message), url=github_repo_url)]
    ]

    await context.bot.send_message(
        chat_id = update.effective_chat.id, 
        text = the_bot.return_mex("about_0", user, update.message),
        reply_markup = InlineKeyboardMarkup(inline_keyboard), 
        parse_mode = 'MarkdownV2'
    )

async def lista_comandi(the_bot:BotWrapper, user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id = update.effective_chat.id, 
        text = the_bot.return_mex("about_1", user, update.message), 
        parse_mode = 'MarkdownV2'
    )

    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = the_bot.return_mex("lista_comandi", user, update.message), 
        parse_mode = 'MarkdownV2'
    )

async def versione(the_bot:BotWrapper, user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = the_bot.return_mex("versione_intro", user, update.message), 
        parse_mode = 'MarkdownV2'
    )

    await context.bot.send_message(
        chat_id = update.effective_chat.id, 
        text = the_bot.return_mex("versione_news", user, update.message), 
        parse_mode = 'MarkdownV2'
    )