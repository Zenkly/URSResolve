from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from chats_db.surveys import surveysDB

ONE_ROUTE = 1

class EncuestaCommand:
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        surveysDB.crear_tablas_si_no_existen()        
        id = surveysDB.register_user(update.message.from_user.id)        
        id_result = str(id)
        print("NUEVA EJECUCIONS")
        keyboard = [
            [
                InlineKeyboardButton("A1",callback_data="Q1-"+id_result+"-A1"),
                InlineKeyboardButton("A2",callback_data="Q1-"+id_result+"-A2"),
                InlineKeyboardButton("A3",callback_data="Q1-"+id_result+"-A3"),
                InlineKeyboardButton("A4",callback_data="Q1-"+id_result+"-A4"),
                InlineKeyboardButton("A5",callback_data="Q1-"+id_result+"-A5")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)                        

        await update.message.reply_text("First Question, Choose answer", reply_markup=reply_markup)

        return ONE_ROUTE