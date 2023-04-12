from secret_stuff import bot_token
from user_info import UserInfo, KnownUserManager
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

known_users = KnownUserManager('known_users.json')
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = UserInfo(update.effective_user.id, update.effective_user.full_name)

    if not known_users.is_known_user(user):
        known_users.add_user(user)
        
        text = f"Ciao _{user.name}_\."
    else: 
        text = f"Bentornato _{user.name}_\."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='MarkdownV2')

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Piacere dei conoscerti", 
        parse_mode='MarkdownV2'
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_token).build()
    
    start_handler = CommandHandler('start', start)
    about_handler = CommandHandler('about', about)

    application.add_handler(start_handler)
    application.add_handler(about_handler)

    application.run_polling()