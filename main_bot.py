from telegram.ext import ApplicationBuilder, CommandHandler, filters, MessageHandler
# Get access to OS commands
import os
# Print formated logs
import logging

from aicap.extractor import Extractor
from aicap.vectorstore import Vectorstore
from functools import partial

ruta_carpeta = './datatxt'

# Llamada a la función para leer los archivos
documentos = Extractor(ruta_carpeta)
documentos.leer_archivos_en_carpeta()
fragmentar_por_articulo = documentos.fragmentar_contenido()

vectorstore = Vectorstore(fragmentar_por_articulo)

class MyBot:
    # Constructor
    def __init__(self, token):
        # Build application
        self.application = ApplicationBuilder().token(token).build()
        # Invoke register_commands method
        self.register_commands()
        self.start_ai_chat()

    def start(self):
        # Start bot
        self.application.run_polling()

    def register_commands(self):
        # Directory where the commands are stored
        command_fies = os.listdir("./commands/")

        # Register all commands in command_files directory
        for file in command_fies:
            # Filter only .py files
            if file.endswith(".py"):
                # Name without extension
                module_name = file[:-3]                
                # Import each command by name
                command_module = __import__(f"commands.{module_name}", fromlist=[module_name])
                # Get command class
                command_class = getattr(command_module,module_name)
                # Every command has a method excute which defines the action
                command_handler = getattr(command_class,"execute")
                # Define command name to use
                command_name = module_name.lower().replace("command","")
                # Add command to bot
                self.application.add_handler(CommandHandler(command_name,command_handler))            
    
    def start_ai_chat(self):        
        ai_module = __import__("aicap.AiCap",fromlist=["AiCap"])
        ai_class = getattr(ai_module,"AiCap")
        ai_handler = getattr(ai_class,"execute")
        # Handler with vectorstore as aditional argument
        ai_handler_with_vec = partial(ai_handler, vectorstore=vectorstore)
        self.application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND),ai_handler_with_vec))
        




logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    token = os.getenv('BOT_TOKEN')
    bot = MyBot(token)
    bot.start()