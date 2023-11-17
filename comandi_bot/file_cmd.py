# Comando /file
from bot_wrapper import BotWrapper
from user_info import UserInfo

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def execute(the_bot:BotWrapper, user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline_keyboard = [
        [InlineKeyboardButton(the_bot.return_mex("file_cmd_1", user, update.message), callback_data='crea')],
        [InlineKeyboardButton(the_bot.return_mex("file_cmd_2", user, update.message), callback_data='cambia')],
        [InlineKeyboardButton(the_bot.return_mex("file_cmd_3", user, update.message), callback_data='salva')],
        [InlineKeyboardButton(the_bot.return_mex("file_cmd_4", user, update.message), callback_data='cancella')]        
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=the_bot.return_mex("file_cmd_0", user, update.message),
        reply_markup=InlineKeyboardMarkup(inline_keyboard), 
        parse_mode='MarkdownV2'
    )

async def crea(the_bot:BotWrapper, user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=the_bot.return_mex("nome_nuovo_file", user, update.message), 
        parse_mode='MarkdownV2'
    )

async def cambia(the_bot:BotWrapper, user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    active_file = user.get_active_file()
    text = ''

    if active_file != None:
        text = the_bot.return_mex("attiva", user, update.message)
    else:
        text = the_bot.return_mex("attiva_vuoto", user, update.message)

    all_file = user.get_files()
    inline_keyboard = []

    for file in all_file:
        inline_keyboard.append([InlineKeyboardButton(file, callback_data=file)])

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard), 
        parse_mode='MarkdownV2'
    )

async def salva(the_bot:BotWrapper, user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    if user.get_active_file() == None:
        user.change_state('cambia')
        await cambia(the_bot, user, update, context)
        return
    
    # str.partition(_sep:str) ritorna una tupla composta da 3 elementi: (first, separator, rest)
    # first è la stringa prima del separatore
    # separator è la prima occorrenza trovata del separatore
    # rest è la stringa dopo il separatore
    # se la stringa non può essere divisa, rest e separator sono stringhe vuote
    _, _, da_salvare = update.message.text.partition(" ")
    if len(da_salvare) > 0:
        await salva_su_file(the_bot, user, da_salvare, update, context)
        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=the_bot.return_mex("salva", user, update.message), 
        parse_mode='MarkdownV2'
    )

async def salva_su_file(the_bot:BotWrapper, user:UserInfo, da_salvare:str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    user.save(da_salvare)

    await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=the_bot.return_mex("salvato", user, update.message), 
            parse_mode='MarkdownV2'
        )
    
    user.return_to_home_state()

async def cancella(the_bot:BotWrapper, user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_file = user.get_files()
    inline_keyboard = []

    for file in all_file:
        inline_keyboard.append([InlineKeyboardButton(file, callback_data=file)])

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=the_bot.return_mex("cancella", user, update.message), 
        reply_markup=InlineKeyboardMarkup(inline_keyboard), 
        parse_mode='MarkdownV2'
    )