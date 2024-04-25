from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from chats_db.surveys import surveysDB

ONE_ROUTE = 1

class EncuestaCommand:
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        surveysDB.crear_tablas_si_no_existen()        
        id = surveysDB.register_user(update.message.from_user.id)        
        id_result = str(id)
        print("NUEVA EJECUCION")
        keyboard = [
            [
                InlineKeyboardButton("Muy útil",callback_data="Q1-"+id_result+"-A1"),
                InlineKeyboardButton("Útil",callback_data="Q1-"+id_result+"-A2"),
                InlineKeyboardButton("Poco útil",callback_data="Q1-"+id_result+"-A3")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)                        

        await update.message.reply_text("¿Qué tan útil encontraste la información proporcionada por el chatbot sobre titulación y servicio social universitario?", reply_markup=reply_markup)

        return ONE_ROUTE