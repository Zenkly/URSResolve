
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from aicap.aiconsult import AiConsult

class AiCap:    
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE,vectorstore):
            
        consultor = AiConsult(vectorstore=vectorstore)  
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