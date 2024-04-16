from telegram import Update
from telegram.ext import ContextTypes

class StartCommand:
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola!\nSoy un bot de ayuda de la <b>Universidad Rosario Castellanos</b>. Cuéntame tus problemas.", parse_mode="HTML")