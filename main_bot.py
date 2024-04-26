# Telegram handler
from telegram.ext import ApplicationBuilder, CommandHandler, filters, MessageHandler, CallbackQueryHandler,ConversationHandler
# Get access to OS commands
import os
# Print formated logs
import logging
# Adds arguments to Handlers
from functools import partial
# Get dir names
from utils.utils import get_themes
# Get survey command
from survey_handlers.EncuestaCommand import EncuestaCommand
# Get some survey handlers
import survey_handlers.surveyHandlers as svh

# Path to txt data
ruta_carpeta = './datatxt/'

# Themes must be defined here to avoid defining it again each time a message is handled
themes = get_themes(ruta_carpeta)

# Bot class 
class MyBot:
    # Constructor
    def __init__(self, token):
        self.ONE_ROUTE = 1
        # Build application
        self.application = ApplicationBuilder().token(token).build()
        # Register_commands method
        self.register_commands()
        # Config and set ai capabilities
        self.start_ai_chat()
        # Config survey process
        self.config_survey()

    # To run bot
    def start(self):
        # Start bot
        self.application.run_polling()
        
    # Register each command in ./commands
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
                if command_name == "consulta":
                    # Add command to bot                
                    ai_handler_with_vec = partial(command_handler, themes=themes)
                    self.application.add_handler(CommandHandler(command_name,ai_handler_with_vec))
                else:
                    # Add command to bot                
                    self.application.add_handler(CommandHandler(command_name,command_handler))                            
    
    # Confif ai capabilities
    def start_ai_chat(self):                
        ai_module = __import__("aicap.AiCap",fromlist=["AiCap"])
        ai_class = getattr(ai_module,"AiCap")
        ai_handler = getattr(ai_class,"execute")
        ai_theme_selector = getattr(ai_class,"select_theme")
        # Handler with vectorstore as aditional argument
        ai_handler_with_vec = partial(ai_handler, themes=themes)
        ai_theme_selector_with_vec = partial(ai_theme_selector, themes=themes)
        # Add consult and theme selector handlers
        self.application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND) & (~filters.REPLY),ai_handler_with_vec))
        self.application.add_handler(CallbackQueryHandler(ai_theme_selector_with_vec,pattern=r'^[-]?\d*\.?\d+$'))
        
    # Config Survey process
    def config_survey(self):
        # Conversational handler to define sequence
        conv_handler = ConversationHandler(
            #Commands that have access to routes
            entry_points=[CommandHandler("encuesta",EncuestaCommand.execute),CallbackQueryHandler(svh.q1,pattern='^E-.+$')],
            #Only one route
            states={
                self.ONE_ROUTE: [
                    #Each handler is executed when a callback patterned arrives
                    CallbackQueryHandler(svh.q2,pattern="^Q1.+$"),
                    CallbackQueryHandler(svh.q3,pattern="^Q2.+$"),
                    CallbackQueryHandler(svh.end,pattern="^Q3.+$")
                ]
            },
            # If all Handlers returns False, the fallback will be executed
            fallbacks=[CommandHandler("encuesta",EncuestaCommand.execute)],
            # Each conversation belongs to a user
            per_user=True,
            per_message=False
            
        )
        self.application.add_handler(conv_handler)          




logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    token = os.getenv('BOT_TOKEN')
    bot = MyBot(token)
    bot.start()