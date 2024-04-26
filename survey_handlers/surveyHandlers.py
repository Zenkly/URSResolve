from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from chats_db.surveys import surveysDB

ONE_ROUTE = 1

async def q1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    surveysDB.crear_tablas_si_no_existen()        
    query = update.callback_query
    _, user_id = query.data.split("-")
    id = surveysDB.register_user(user_id)        
    id_result = str(id)
    await query.answer()    
    keyboard = [
        [
            InlineKeyboardButton("Muy útil",callback_data="Q1-"+id_result+"-A1"),
            InlineKeyboardButton("Útil",callback_data="Q1-"+id_result+"-A2"),
            InlineKeyboardButton("Poco útil",callback_data="Q1-"+id_result+"-A3")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)       
    question = "¿Qué tan útil encontraste la información proporcionada por el chatbot sobre titulación y servicio social universitario?"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=question,reply_markup=reply_markup)    
    return ONE_ROUTE

async def q2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    question, id, answer = query.data.split("-")
    print(question,id,answer)
    surveysDB.register_answer(id,question,answer)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Muy claras y comprensibles",callback_data="Q2-"+id+"-A1"),
            InlineKeyboardButton("Claras y comprensibles",callback_data="Q2-"+id+"-A2"),
            InlineKeyboardButton("Poco claras y comprensibles",callback_data="Q2-"+id+"-A3")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="¿Cómo calificarías la claridad y comprensibilidad de las respuestas del chatbot sobre estos procesos?",reply_markup=reply_markup)
    return ONE_ROUTE

async def q3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    question, id, answer = query.data.split("-")
    print(question,id,answer)
    surveysDB.register_answer(id,question,answer)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Sí, completamente",callback_data="Q3-"+id+"-A1"),
            InlineKeyboardButton("Sí, en su mayoría",callback_data="Q3-"+id+"-A2"),
            InlineKeyboardButton("No del todo",callback_data="Q3-"+id+"-A3")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="¿El chatbot satisfizo todas tus necesidades de información sobre titulación y servicio social universitario?",reply_markup=reply_markup)
    return ONE_ROUTE

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    question, id, answer = query.data.split("-")
    print(question,id,answer)
    surveysDB.register_answer(id,question,answer)
    await query.answer()
    await query.edit_message_text(text="¡Gracias por compartirnos tu opinión!")
    return ConversationHandler.END