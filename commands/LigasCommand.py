from telegram import Update
from telegram.ext import ContextTypes

class LigasCommand:
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        response = """
        *Enlaces de Interés*
       
        [Ejemplo](https://www.example.com)
        
        [Google](https://www.google.com)
        
        [Página Oficial de la URC](https://rcastellanos.cdmx.gob.mx/)
        
        """
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode="MarkdownV2")