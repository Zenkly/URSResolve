# Telegram handler
from telegram.ext import ApplicationBuilder, CommandHandler
import os

token = os.getenv('BOT_TOKEN')


async def start_command(update, context):
    await update.message.reply_text("Hi. I'm a test bot")

async def help_command(update, context):
    await update.message.reply_text("if you need help! search on Google")

def main():
  app = ApplicationBuilder().token(token).read_timeout(30).write_timeout(30).build()

  app.add_handler(CommandHandler("start", start_command))
  app.add_handler(CommandHandler("help", help_command))

  app.run_polling()


if __name__ == '__main__':
   main()