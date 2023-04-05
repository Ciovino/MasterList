from secret_stuff import bot_token
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

known_users = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in known_users:
        known_users.append(user.id)
        text = f"Ciao _{user.full_name}_\."
    else: 
        text = f"Bentornato _{user.full_name}_\."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='MarkdownV2')

if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()