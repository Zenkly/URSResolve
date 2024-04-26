from telegram import Update
from telegram.ext import ContextTypes
from chats_db.userTypes import userTypesDB as udb

class RadminCommand:
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        udb.crear_tablas_si_no_existen()
        admin = "@" + update.message.from_user.username        
        users = update.effective_message.parse_entities(["mention"])        
        for user in users.values():
            udb.register_user(user)            
            response = udb.set_admin(admin,user)                                     
        if response == 0:
            await update.message.reply_text(text="Usuarios registrados" )
        else: 
            await update.message.reply_text(text="Hubo un error al registrar al usuario. *¿Eres administrador?*" )