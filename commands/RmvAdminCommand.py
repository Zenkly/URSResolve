from telegram import Update
from telegram.ext import ContextTypes
from chats_db.userTypes import userTypesDB as udb

class RmvAdminCommand:
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        udb.crear_tablas_si_no_existen()
        admin = "@" + update.message.from_user.username
        users = update.effective_message.parse_entities(["mention"])
        try:            
            for user in users.values():                           
                udb.unset_admin(admin,user)                                     
            await update.message.reply_text(text="Administradores removidos" )
        except Exception as e:
                    print("Ocurrio un error:",type(e).__name__)
                    print(e)
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hubo un error al eliminar el usuario")