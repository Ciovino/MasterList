import secret_stuff as bot_info
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = f"Ciao {user.full_name}. Come straminchia stai?"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

if __name__ == '__main__':
    application = ApplicationBuilder()
    application.token(bot_info.mov_list_token)
    application.build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()