from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

ONE_ROUTE = 1

async def q1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    question, id, answer = query.data.split("-")
    print(question,id,answer)
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
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("A1",callback_data="Q2-"+id+"-A1"),
            InlineKeyboardButton("A2",callback_data="Q2-"+id+"-A2"),
            InlineKeyboardButton("A3",callback_data="Q2-"+id+"-A3"),
            InlineKeyboardButton("A4",callback_data="Q2-"+id+"-A4"),
            InlineKeyboardButton("A5",callback_data="Q2-"+id+"-A5")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Second Question, Choose answer",reply_markup=reply_markup)
    return ONE_ROUTE

async def q3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    question, id, answer = query.data.split("-")
    print(question,id,answer)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("A1",callback_data="Q3-"+id+"-A1"),
            InlineKeyboardButton("A2",callback_data="Q3-"+id+"-A2"),
            InlineKeyboardButton("A3",callback_data="Q3-"+id+"-A3"),
            InlineKeyboardButton("A4",callback_data="Q3-"+id+"-A4"),
            InlineKeyboardButton("A5",callback_data="Q3-"+id+"-A5")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Third Question, Choose answer",reply_markup=reply_markup)
    return ONE_ROUTE

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    question, id, answer = query.data.split("-")
    print(question,id,answer)
    await query.answer()
    await query.edit_message_text(text="See you next time!")
    return ConversationHandler.END