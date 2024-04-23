
from telegram import Update, ForceReply
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from aicap.aiconsult import AiConsult
from chats_db.history import historyDB

class AiCap:    
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE,themes):
        historyDB.crear_tablas_si_no_existen()
        theme = historyDB.get_theme(update.message.from_user.id)
        if theme:
            if theme == "expired":
                response = "El tema de nuestra conversación ha expirado, elige uno de los siguientes temas:\n"
                for key in themes:
                    response = response + f"● {key}"
                await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
            else:                            
                print(theme)
                consultor = AiConsult(vectorstore=themes[theme])  
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
            for key in themes:
                response = response + f"● {key}"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=response,reply_markup=ForceReply())
            theme = list(themes.keys())[0]
            historyDB.set_theme(update.message.from_user.id,theme)
            

        
        