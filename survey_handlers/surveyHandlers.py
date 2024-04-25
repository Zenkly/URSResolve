from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from chats_db.surveys import surveysDB

ONE_ROUTE = 1

async def q1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    question, id, answer = query.data.split("-")
    print(question.lower(),int(id),answer)
    surveysDB.register_answer(id,question,answer)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("A1",callback_data="Q1-"+id+"-A1"),
            InlineKeyboardButton("A2",callback_data="Q1-"+id+"-A2"),
            InlineKeyboardButton("A3",callback_data="Q1-"+id+"-A3"),
            InlineKeyboardButton("A4",callback_data="Q1-"+id+"-A4"),
            InlineKeyboardButton("A5",callback_data="Q1-"+id+"-A5")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="First Question, Choose answer",reply_markup=reply_markup)
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