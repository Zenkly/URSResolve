from telegram import Update
from telegram.ext import ContextTypes

class StartCommand:
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = """
¡Saludos y bienvenido!\n
( ˘▽˘)っ\n
Soy Castell, un bot de ayuda de desarrollado por estudiantes de la <b>Universidad Rosario Castellanos</b>.
Aquí tienes acceso a información relevante sobre nuestra universidad.

Podemos ayudarte con información de procedimientos acerca de:

- Proceso de admisión.
- Proceso de titulación.
- Requisitos y procedimientos del servicio social.
- Oferta académica.
- Lineamientos y normativas institucionales.

Para comenzar una consulta en un chat privado simplemente envía un mensaje - Puedes decir simplemente "Hola" (>‿◠)✌ - y se desplegará el menú de temas.
También puedes puedes utilizar los siguientes comandos:\n
/start Para mostrar nuevamente este mensaje
/consulta Para realizar consultas en chats grupales
/encuesta Para ayudarnos contestando una breve encuesta de satisfacción
/ligas Para mostrar algunas ligas que pueden ser de tu interés como estudiante de la URC

Espero poder ayudarte con tus dudas.\n
ヽ(•‿•)ノ
"""
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")