
from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from aicap.aiconsult import AiConsult
from chats_db.history import historyDB

class AiCap:    
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE,themes):
        if (update.effective_chat.type != "private") and (update.effective_chat.type != "group"):
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
                    preamble = themes[theme]["preamble"]
                    consultor = AiConsult(vectorstore=themes[theme]["vectorstore"],preamble=preamble)  
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="Lo siento parece que la base ha cambiado. Vuelve a elegir el tema.")
                    historyDB.unset_theme(update.message.from_user.id)
                    return
                try:

                    if(update.effective_chat.type == "private"):                
                        message = update.message.text
                    elif(update.effective_chat.type == "group"):                            
                        message = update.message.text.replace("/consulta","")
                    keyboard = [[InlineKeyboardButton("Cambiar tema",callback_data=-1)]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    response = consultor.consultOpenAi(update.message.from_user.id,message)
                    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING)
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=response,reply_markup=reply_markup)                
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
            if query.data.lstrip('-').isdigit():
                option_number = int(query.data)
                print("Option Number:")
                print(option_number)
                if (option_number>=0) and (option_number < len(themes_list)):
                    theme = themes_list[option_number]                    
                    historyDB.set_theme(query.from_user.id,theme)
                    await query.edit_message_text(text=f"De acuerdo cuéntame tus dudas de {themes_list[option_number]}")
                if option_number==-1:
                    print("Cambiando tema")
                    historyDB.unset_theme(query.from_user.id)
                    await context.bot.send_message(query.message.chat.id,text=f"Fue un placer ayudarte. Envía otro mensaje para iniciar otra conversación.")
            

    def format_options(themes):
        themes_list = list(themes.keys())
        keyboard = []
        for i in range(len(themes_list)):
            keyboard.append([InlineKeyboardButton(themes_list[i],callback_data=i)])
        return keyboard
        

            

        
        