
from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from aicap.aiconsult import AiConsult
from chats_db.history import historyDB

class AiCap:    
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE,themes):
        if not (update.effective_chat.type == "private") or not (update.effective_chat.type == "group"):
            return
        historyDB.crear_tablas_si_no_existen()
        #print(update.message)
        theme = historyDB.get_theme(update.message.from_user.id)
        if theme:
            if theme == "expired":
                response = "El tema de nuestra conversación ha expirado, elige uno de los siguientes temas:\n"
                # for key in themes:
                #     response = response + f"● {key}"
                keyboard = AiCap.format_options(themes)
                reply_markup = InlineKeyboardMarkup(keyboard)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=response,reply_markup=reply_markup)
                # if option:
                #     print(option)
                #     AiCap.select_theme(update.message.from_user.id,option.text,themes)
                
            else:                            
                print(theme)
                if theme in themes.keys():
                    consultor = AiConsult(vectorstore=themes[theme])  
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="Lo siento parece que la base ha cambiar. Vuelve a elegir el tema.")
                    historyDB.uset_theme(update.message.from_user.id)
                    return
                try:
                    if(update.effective_chat.type == "private"):                
                        #response = consultor.consult(update.message.from_user.id,update.message.text)
                        response = consultor.consultOpenAi(update.message.from_user.id,update.message.text)
                        #print("OK AICAP")
                        #print(response)
                        await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING)
                        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
                    elif(update.effective_chat.type == "group"):                            
                        message = update.message.text.replace("/consulta","")
                        response = consultor.consultOpenAi(update.message.from_user.id,message)
                        await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING)
                        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)                
                except Exception as e:
                    print("Ocurrio un error:",type(e).__name__)
                    print(e)
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="Has superado la cuota o la AI parece no estar disponible.")
        else:
            response = "¡Hola! Antes de poder ayudarte debes elegir entre uno de los siguientes temas:\n"
            keyboard = AiCap.format_options(themes)
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=response,reply_markup=reply_markup)
            # if option:
            #     print(option)
            #     AiCap.select_theme(update.message.from_user.id,option.text,themes)

    async def select_theme(update: Update, context: ContextTypes.DEFAULT_TYPE,themes):
            query = update.callback_query
            print("query:")
            print(query)
            await query.answer()

            themes_list = list(themes.keys())
            if query.data.isdigit():
                option_number = int(query.data)
                if (option_number>=0) and (option_number < len(themes_list)):
                    theme = themes_list[option_number]                    
                    historyDB.set_theme(query.from_user.id,theme)
            await query.edit_message_text(text=f"De acuerdo cuéntame tus dudas de {themes_list[option_number]}")

    def format_options(themes):
        themes_list = list(themes.keys())
        keyboard = []
        for i in range(len(themes_list)):
            keyboard.append([InlineKeyboardButton(themes_list[i],callback_data=i)])
        return keyboard
        

            

        
        