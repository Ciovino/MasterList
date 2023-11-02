from secret_stuff import bot_token, github_repo_url
from user_info import UserInfo
from known_user_manager import KnownUserManager
from mex_manager import MexManager
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

known_users = KnownUserManager('bot\\known_users.json')
mex_manager = MexManager('bot\\bot_mex.json')

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Recupera le info dell'utente, se ha già usato il comando start
    user = known_users.is_known_user(update.effective_user.id)

    if user is None:
        # Aggiungi l'utente se è nuovo
        user = known_users.add_user(UserInfo(update.effective_user.id, update.effective_user.full_name, "start", []))
        
        text = mex_manager.return_mex("primo_saluto", user, update.message)
    else:
        # Controlla lo stato dell'utente
        if user.state != "start":
            # L'utente è impegnato in un altro comando
            return
    
        text = mex_manager.return_mex("saluto", user, update.message)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=text, 
        parse_mode='MarkdownV2'
    )

async def unknown_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=mex_manager.return_mex("sconosciuto", None, update.message), 
        parse_mode='MarkdownV2'
    )

# Comando /file
async def file_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Recupera le info dell'utente
    user = known_users.is_known_user(update.effective_user.id)

    if user == None:
        await unknown_user(update, context)
        return

    # Controlla lo stato dell'utente
    if user.state == "start":
        # Cambia lo stato in 'file'
        user.state = "file"

        inline_keyboard = [
            [InlineKeyboardButton(mex_manager.return_mex("file_cmd_1", user, update.message), callback_data='new_file')],
            [InlineKeyboardButton(mex_manager.return_mex("file_cmd_2", user, update.message), callback_data='change_active')],
            [InlineKeyboardButton(mex_manager.return_mex("file_cmd_3", user, update.message), callback_data='save_file')],
            [InlineKeyboardButton(mex_manager.return_mex("file_cmd_4", user, update.message), callback_data='delete_file')]
        ]

        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=mex_manager.return_mex("file_cmd_0", user, update.message),
            reply_markup=InlineKeyboardMarkup(inline_keyboard), 
            parse_mode='MarkdownV2'
        )

# Creazione di un nuovo file
async def new_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Recupera le info dell'utente
    user = known_users.is_known_user(update.effective_user.id)

    if user == None:
        await unknown_user(update, context)
        return

    # Controlla lo stato dell'utente
    if user.state == "new_file":
        # Crea il file
        if user.add_file(update.message.text):
            # File creato
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=mex_manager.return_mex("nuovo_file", user, update.message), 
                parse_mode='MarkdownV2'
            )

            known_users.save_users()
        else:
            # File non creato
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=mex_manager.return_mex("no_file", user, update.message), 
                parse_mode='MarkdownV2'
            )

        # Reimposta lo stato
        user.state = "start"
    elif user.state == "save":
        user.save(update.message.text)

        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=mex_manager.return_mex("salvato", user, update.message), 
            parse_mode='MarkdownV2'
        )

        user.state = "start"
    elif user.state == "change_active":
        return

async def save_on_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Recupera le info dell'utente
    user = known_users.is_known_user(update.effective_user.id)

    if user == None:
        await unknown_user(update, context)
        return

    # Reimposta lo stato
    user.state = "save"

    if user.get_active_file() == None:
        await change_active_file(user, update, context)
        return
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=mex_manager.return_mex("salva", user, update.message), 
        parse_mode='MarkdownV2'
    )

async def delete_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Recupera le info dell'utente
    user = known_users.is_known_user(update.effective_user.id)

    if user == None:
        await unknown_user(update, context)
        return

    # Reimposta lo stato
    user.state = "delete"

    all_file = user.get_files()
    inline_keyboard = []

    for file in all_file:
        inline_keyboard.append([InlineKeyboardButton(file, callback_data=file)])
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=mex_manager.return_mex("cancella", user, update.message), 
        reply_markup=InlineKeyboardMarkup(inline_keyboard), 
        parse_mode='MarkdownV2'
    )

# Comando /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Recupera le info dell'utente
    user = known_users.is_known_user(update.effective_user.id)

    if user == None:
        await unknown_user(update, context)
        return

    # Reimposta lo stato
    user.state = "start"

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=mex_manager.return_mex("back", user, update.message), 
        parse_mode='MarkdownV2'
    )

# Comando /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = known_users.is_known_user(update.effective_user.id)
    if user == None:
        await unknown_user(update, context)
        return

    inline_keyboard = [
        [InlineKeyboardButton(mex_manager.return_mex("about_1", user, update.message), callback_data='comandi_spiegazione')],
        [InlineKeyboardButton(mex_manager.return_mex("about_2", user, update.message), callback_data='versione')],
        [InlineKeyboardButton(mex_manager.return_mex("about_3", user, update.message), url=github_repo_url)]
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=mex_manager.return_mex("about_0", user, update.message),
        reply_markup=InlineKeyboardMarkup(inline_keyboard), 
        parse_mode='MarkdownV2'
    )

# Rispondi alle CallBackQuery
async def command_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = known_users.is_known_user(update.effective_user.id)

    if user == None:
        await unknown_user(update, context)
        return

    query = update.callback_query

    await query.answer()
    await query.delete_message()

    # Controlla la query
    if query.data == "comandi_spiegazione":
        # Messaggio con la spiegazione dei comandi
        await mex_command_list(user, update, context)
    elif query.data == "versione":
        # Messaggio con le informazioni riguardanti la versione attuale del bot
        await mex_bot_version(user, update, context)
    elif query.data == "new_file":
        # Crea un nuovo file
        user.state = 'new_file'
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=mex_manager.return_mex("nome_nuovo_file", user, update.message), 
            parse_mode='MarkdownV2'
        )
    elif query.data == "change_active":
        # Cambia il file attivo (file in cui viene salvata la roba)
        await change_active_file(user, update, context)
    elif query.data == "save_file":
        # Salva su file attivo
        await save_on_file(update, context)
    elif query.data == "delete_file":
        # Cancella un file
        await delete_file(update, context)
    else:
        # Cambia file attivo
        if user.state == "change_active":
            if user.change_active(query.data):
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, 
                    text=mex_manager.return_mex("attivato", user, update.message), 
                    parse_mode='MarkdownV2'
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, 
                    text=mex_manager.return_mex("non_attivato", user, update.message), 
                    parse_mode='MarkdownV2'
                )
        # Cancella un file
        elif user.state == "delete":
            if user.delete_file(query.data):
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, 
                    text=mex_manager.return_mex("eliminato", user, update.message),
                    parse_mode="Markdownv2"
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, 
                    text=mex_manager.return_mex("non_eliminato", user, update.message), 
                    parse_mode="Markdownv2"
                )
            
            known_users.save_users()
        
        user.state = 'start'

async def mex_command_list(user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=mex_manager.return_mex("about_1", user, update.message), 
        parse_mode='MarkdownV2'
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=mex_manager.return_mex("lista_comandi", user, update.message), 
        parse_mode='MarkdownV2'
    )

async def mex_bot_version(user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=mex_manager.return_mex("versione_intro", user, update.message), 
        parse_mode='MarkdownV2'
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=mex_manager.return_mex("versione_news", user, update.message), 
        parse_mode='MarkdownV2'
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=mex_manager.return_mex("versione_bug", user, update.message), 
        parse_mode='MarkdownV2', 
        disable_web_page_preview=True
    )

async def change_active_file(user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    user.state = 'change_active'

    active_file = user.get_active_file()
    text = ''
    if active_file != None:
        text = mex_manager.return_mex("attiva", user, update.message)
    else:
        text = mex_manager.return_mex("attiva_vuoto", user, update.message)
    
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

if __name__ == '__main__':
    # Crea il bot
    application = ApplicationBuilder().token(bot_token).build()
    
    # Comando /start
    start_handler = CommandHandler('start', start)
    
    # Comando /file
    file_handler = CommandHandler('file', file_cmd)

    # Comando /save
    save_handler = CommandHandler('save', save_on_file)

    # Comando /delete
    delete_handler = CommandHandler('delete', delete_file)

    # Comando /about
    about_handler = CommandHandler('about', about)
    command_list_handler = CallbackQueryHandler(command_list)

    # Comando /cancel
    cancel_handler = CommandHandler('back', cancel)

    # Prendi il nome del nuovo file da creare
    new_file_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), new_file)

    application.add_handler(new_file_handler)
    application.add_handler(start_handler)
    application.add_handler(file_handler)
    application.add_handler(save_handler)
    application.add_handler(delete_handler)
    application.add_handler(cancel_handler)
    application.add_handler(about_handler)
    application.add_handler(command_list_handler)

    application.run_polling()