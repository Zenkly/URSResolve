from telegram import Update
from telegram.ext import ContextTypes
from chats_db.surveys import surveysDB as sdb
from chats_db.userTypes import userTypesDB as udb

class Dsurveys:
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        sdb.crear_tablas_si_no_existen()
        udb.crear_tablas_si_no_existen()
        user = "@"+ update.message.from_user.username
        if udb.is_admin(user):
            sdb.export_to_csv(update.message.from_user.id)
            await context.bot.send_document(chat_id=update.effective_chat.id,document='./chats_db/surveysTable.csv')
        else:
            await update.message.reply_text(text="No estas autorizado para ejecutar este comando")