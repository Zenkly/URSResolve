from telegram import Update
from telegram.ext import ContextTypes
from aicap.AiCap import AiCap
# Adds arguments to Handlers
from functools import partial

class ConsultaCommand:
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE,vectorstore):
        print(update)
        print(context)
        await AiCap.execute(update,context,vectorstore)