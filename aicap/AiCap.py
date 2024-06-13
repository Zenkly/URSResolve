
from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from aicap.aiconsult import AiConsult
from chats_db.history import historyDB
from chats_db.surveys import surveysDB as sdb

# Ai capabilities object
class AiCap:        
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE,themes):
        sdb.crear_tablas_si_no_existen()
        if (update.effective_chat.type != "private") and (update.effective_chat.type != "group"):
            return
        # Previous Message Database
        historyDB.crear_tablas_si_no_existen()        
        # Get theme from previous messages
        theme = historyDB.get_theme(update.message.from_user.id)
        # If previous theme exist
        if theme:
            # If previous theme expired
            if theme == "expired":
                response = "El tema de nuestra conversación ha expirado, elige uno de los siguientes temas:\n"
                # Keyboard of theme buttons
                keyboard = AiCap.format_options(themes)
                # Send a message and a formated keyboard 
                reply_markup = InlineKeyboardMarkup(keyboard)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=response,reply_markup=reply_markup)
            # If current topic exists
            else:                            
                # Verify if theme exists in themes array
                if theme in themes.keys():
                    # Get theme preamble
                    preamble = themes[theme]["preamble"]
                    # Create a Consultor with vectortore and preamble by topic
                    consultor = AiConsult(vectorstore=themes[theme]["vectorstore"],preamble=preamble)  
                # Theme do not exist (maybe deled)
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="Lo siento parece que la base ha cambiado. Vuelve a elegir el tema.")
                    historyDB.unset_theme(update.message.from_user.id)
                    return
                try:
                    # Detect chat type to extract user request
                    if(update.effective_chat.type == "private"):                
                        message = update.message.text
                    elif(update.effective_chat.type == "group"):                            
                        message = update.message.text.replace("/consulta","")

                    #Create a keyboard for change topic and make a satisfaction survey
                    keyboard = [[InlineKeyboardButton("Cambiar tema",callback_data=-1)]]

                    # #Add survey button only id user didn't answer the survey previously
                    if not sdb.user_answered_survey(update.message.from_user.id):
                        id = update.message.from_user.id
                        keyboard.append([InlineKeyboardButton("Ayudanos con una encuesta 🗳",callback_data="E-"+str(id))])
                    
                    # print(sdb.user_answered_survey(update.message.from_user.id))
                    # id = update.message.from_user.id
                    # keyboard.append([InlineKeyboardButton("Ayudanos con una encuesta 🗳",callback_data="E-"+str(id))])

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
                    await query.edit_message_text(text=f"(* ˘⌣˘)◞ ¡Gracias!. Estoy listo ahora puedes escribirme tus dudas de {themes_list[option_number]}")
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
        

            

        
        