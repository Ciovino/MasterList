from secret_stuff import bot_token, github_repo_url
from user_info import UserInfo
from known_user_manager import KnownUserManager
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

known_users = KnownUserManager('known_users.json')

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Recupera le info dell'utente, se ha già usato il comando start
    user = known_users.is_known_user(update.effective_user.id)

    if user is None:
        # Aggiungi l'utente se è nuovo
        user = known_users.add_user(UserInfo(update.effective_user.id, update.effective_user.full_name, "start", []))
        
        text = f"Ciao _{user.name}_\."
    else:
        # Controlla lo stato dell'utente
        if user.state != "start":
            # L'utente è impegnato in un altro comando
            return
    
        text = f"Bentornato _{user.name}_\."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='MarkdownV2')

async def unknown_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Ciao _{update.effective_user.full_name}_\.Per cominciare ad usare il bot, usa il comando /start', parse_mode='MarkdownV2')

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
            [InlineKeyboardButton("Nuovo file", callback_data='new_file')],
            [InlineKeyboardButton("Cambia file attivo", callback_data='change_active')],
            [InlineKeyboardButton("Salva robe", callback_data='save_file')],
            [InlineKeyboardButton("Scancellamento", callback_data='delete_file')]
        ]

        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Cosa vuoi fare?",
            reply_markup=InlineKeyboardMarkup(inline_keyboard)
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
                text=f"Nuovo file creato: {(update.message.text).replace(' ', '_').lower()}.json"
            )

            known_users.save_users()
        else:
            # File non creato
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=f"Sorry. Non posso creare il file"
            )

        # Reimposta lo stato
        user.state = "start"
    elif user.state == "save":
        user.save(update.message.text)

        await context.bot.send_message(chat_id=update.effective_chat.id, text="Salvato")

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
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Scrivi quello che vuoi salvare")

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
        text="Quale file vuoi cancellare?", 
        reply_markup=InlineKeyboardMarkup(inline_keyboard)
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
        text="Operazione annullata\nRIPETO\nOPERAZIONE ANNULLATA"
    )

# Comando /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = f"Ciao _{update.effective_user.full_name}_\.\nSono _MovList_ e ti aiuterò a gestire film e serie TV che hai intenzione di guardare\."
    inline_keyboard = [
        [InlineKeyboardButton("Lista completa dei comandi", callback_data='comandi_spiegazione')],
        [InlineKeyboardButton("Lista delle features in arrivo", callback_data='nuove_features')],
        [InlineKeyboardButton("Repository GitHub", url=github_repo_url)]
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=about_text, 
        parse_mode='MarkdownV2',
        reply_markup=InlineKeyboardMarkup(inline_keyboard)
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
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Lista completa dei comandi")

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="_/start_: Manda un saluto all'utente;\n_/about_: Presentazione\.",
            parse_mode='MarkdownV2'
        )
    elif query.data == "nuove_features":
        # Messaggio con tutte le nuove features in programma
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Al momento non c'è nulla in programma")
    elif query.data == "new_file":
        # Crea un nuovo file
        user.state = 'new_file'
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Scrivi il nome del file")
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
                await context.bot.send_message(chat_id=update.effective_chat.id, text="File attivato")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Impossibile attivare il file")
        # Cancella un file
        elif user.state == "delete":
            if user.delete_file(query.data):
                await context.bot.send_message(chat_id=update.effective_chat.id, text="File eliminato")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Impossibile eliminare il file")
            
            known_users.save_users()
        
        user.state = 'start'

async def change_active_file(user:UserInfo, update: Update, context: ContextTypes.DEFAULT_TYPE):
    user.state = 'change_active'

    active_file = user.get_active_file()
    text = ''
    if active_file != None:
        text = f'File attivo: {active_file}.\nQuale file vuoi attivare?'
    else:
        text = f'Nessun file attivo.\nQuale file vuoi attivare?'
    
    all_file = user.get_files()
    inline_keyboard = []

    for file in all_file:
        inline_keyboard.append([InlineKeyboardButton(file, callback_data=file)])
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=text, 
        reply_markup=InlineKeyboardMarkup(inline_keyboard)
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