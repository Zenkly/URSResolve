from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from chats_db.surveys import surveysDB

class EncuestaCommand:
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        surveysDB.crear_tablas_si_no_existen()
        result = surveysDB.register_user(update.message.from_user.id)
        message = update.message.text.replace("/consulta","")
        keyboard = [
            [InlineKeyboardButton("A1",callback_data="a"),InlineKeyboardButton("A2",callback_data="b"),InlineKeyboardButton("A3",callback_data="c")],
            [InlineKeyboardButton("A4",callback_data="d"),InlineKeyboardButton("A5",callback_data="e"),InlineKeyboardButton("A6",callback_data="f")]
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)                
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Q1",reply_markup=reply_markup)                