from secret_stuff import bot_token
from user_info import UserInfo
from bot_wrapper import BotWrapper
from comandi_bot import state_cmd, back_cmd, start_cmd, about_cmd, file_cmd

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

list_bot = BotWrapper('bot\\known_users.json', 'bot\\bot_mex.json')

async def main_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = list_bot.is_known_user(update.effective_user.id)
    if user == None:
        user = list_bot.add_user(UserInfo(update.effective_user.id, update.effective_user.full_name, []))

    command = update.message.text.split(' ')[0].removeprefix('/')

    if not user.is_valid_command(command):
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "comando non valido"
        )
        return
    
    if not user.change_state(command):
        """await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "impossibile cambiare stato"
        )"""
        return

    if command == 'back':
        await back_cmd.execute(list_bot, user, update, context)
        return

    if command == 'start':
        await start_cmd.execute(list_bot, user, update, context)
        return

    if command == 'state':
        await state_cmd.execute(list_bot, user, update, context)
        return
    
    if command == 'about':
        await about_cmd.execute(list_bot, user, update, context)
        return
    
    if command == 'file':
        await file_cmd.execute(list_bot, user, update, context)
        return
    
    if command == 'crea':
        await file_cmd.crea(list_bot, user, update, context)
        return

    if command == 'cambia':
        await file_cmd.cambia(list_bot, user, update, context)
        return
    
    if command == 'salva':
        await file_cmd.salva(list_bot, user, update, context)
        return    

    if command == 'mostra':
        await file_cmd.mostra(list_bot, user, update, context)
        return
    
    if command == 'cancella':
        await file_cmd.cancella(list_bot, user, update, context)
        return
    
    if command == 'modifica':
        await file_cmd.modifica(list_bot, user, update, context)
        return
    
    if command == 'elimina':
        await file_cmd.elimina(list_bot, user, update, context)
        return

async def normal_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = list_bot.is_known_user(update.effective_user.id)
    if user == None:
        user = list_bot.add_user(UserInfo(update.effective_user.id, update.effective_user.full_name, []))
    
    if not user.is_mex_state():
        return

    state = user.get_current_state()
    
    if state == 'crea':
        if user.add_file(update.message.text):
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=list_bot.return_mex("nuovo_file", user, update.message), 
                parse_mode='MarkdownV2'
            )

            list_bot.save_user()
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=list_bot.return_mex("no_file", user, update.message), 
                parse_mode='MarkdownV2'
            )
        
        user.return_to_home_state()
        return

    if state == 'salva':
        await file_cmd.salva_su_file(list_bot, user, update.message.text, update, context)
        return
    
    if state == 'cancella':
        try:
            riga_da_cancellare = int(update.message.text)
            riga_cancellata = user.delete_line(riga_da_cancellare)

            if riga_cancellata < 0:
                # La riga non è stata cancellata perchè il numero inserito era fuori dai limiti
                messaggio = list_bot.return_mex("fuori_limite", user, update.message)
            else:
                messaggio = list_bot.return_mex("cancellata", user, update.message)
                user.return_to_home_state()
        except ValueError:
            messaggio = list_bot.return_mex("value_error", user, update.message)

        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = messaggio
        )
        return
    
    if state == 'modifica':
        try:
            riga_da_modificare = int(update.message.text)

            if riga_da_modificare <= 0 or riga_da_modificare > len(user.show()):                
                messaggio = list_bot.return_mex("fuori_limite", user, update.message)
            else:
                messaggio = list_bot.return_mex("modifica_in_corso", user, update.message)
                list_bot.modify_line(riga_da_modificare-1)
                user.change_state('modifica_in_corso')
        except ValueError:
            messaggio = list_bot.return_mex("value_error", user, update.message)

        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = messaggio
        )
        return
    
    if state == 'modifica_in_corso':
        if user.save_at_index(update.message.text, list_bot.get_modified_line()):
            messaggio = list_bot.return_mex("modifica_fatta", user, update.message)
        else:
            messaggio = list_bot.return_mex("modifica_fallita", user, update.message)

        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = list_bot.return_mex("modifica_fatta", user, update.message)
        )

        user.return_to_home_state()
        return

async def callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = list_bot.is_known_user(update.effective_user.id)
    if user == None:
        user = list_bot.add_user(UserInfo(update.effective_user.id, update.effective_user.full_name, []))    

    query = update.callback_query

    await query.answer()
    ## await query.delete_message()

    if not user.is_query_state():
        return

    state = user.get_current_state()
    
    if state == 'about':
        if query.data == 'lista_comandi':
            await about_cmd.lista_comandi(list_bot, user, update, context)
        elif query.data == 'versione':
            await about_cmd.versione(list_bot, user, update, context)

        user.return_to_home_state()
        return
    
    if state == 'file':
        if query.data == 'crea':
            user.change_state('crea')
            await file_cmd.crea(list_bot, user, update, context)

        elif query.data == 'cambia':
            user.change_state('cambia')
            await file_cmd.cambia(list_bot, user, update, context)

        elif query.data == 'salva':
            user.change_state('salva')
            await file_cmd.salva(list_bot, user, update, context)

        elif query.data == 'elimina':
            user.change_state('elimina')
            await file_cmd.elimina(list_bot, user, update, context)

        return
    
    if state == 'cambia':
        if user.change_active(query.data):
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=list_bot.return_mex("attivato", user, update.message), 
                parse_mode='MarkdownV2'
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=list_bot.return_mex("non_attivato", user, update.message), 
                parse_mode='MarkdownV2'
            )
        
        user.return_to_home_state()
        return
    
    if state == 'mostra':
        if query.data == 'back':
            user.change_state('back')
            await back_cmd.execute(list_bot, user, update, context)

        elif query.data == 'cancella':
            user.change_state('cancella')
            await file_cmd.cancella(list_bot, user, update, context)

        elif query.data == 'modifica':
            user.change_state('modifica')
            await file_cmd.modifica(list_bot, user, update, context)

        return

    if state == 'elimina':
        if user.delete_file(query.data):
            await context.bot.send_message(
                    chat_id=update.effective_chat.id, 
                    text=list_bot.return_mex("eliminato", user, update.message),
                    parse_mode="Markdownv2"
                )
            
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text=list_bot.return_mex("non_eliminato", user, update.message), 
                parse_mode="Markdownv2"
            )
        
        list_bot.save_user()

        user.return_to_home_state()
        return

if __name__ == '__main__':
    # Crea il bot
    application = ApplicationBuilder().token(bot_token).build()

    # Comandi
    main_command_handler = MessageHandler(filters.COMMAND, main_command)
    application.add_handler(main_command_handler)

    # Messaggi normali
    normal_message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), normal_message)
    application.add_handler(normal_message_handler)

    # Callback query
    callback_query_handler = CallbackQueryHandler(callback_query)
    application.add_handler(callback_query_handler)

    # Avvia il bot
    application.run_polling()