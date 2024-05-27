from telegram import Update
from telegram.ext import ContextTypes

class LigasCommand:
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        response = """
        *Enlaces de Interés*
       
        [Página Oficial de la URC](https://rcastellanos.cdmx.gob.mx/)
        
        [Oferta académica](https://www.rcastellanos.cdmx.gob.mx/ofertaacademica)

        *Calendarios académicos:*
        [Presencial - híbrida](https://www.rcastellanos.cdmx.gob.mx/storage/app/media/CalendarioEscolar2024PH.pdf)
        [A Distancia - Híbrida](https://www.rcastellanos.cdmx.gob.mx/storage/app/media/CalendarioEscolar2024LAD.pdf)
        [Semipresencial](https://www.rcastellanos.cdmx.gob.mx/storage/app/media/CalendarioEscolar2024SP.pdf)

        [Marco Normativo](https://www.rcastellanos.cdmx.gob.mx/dependencia/marco-normativo)

        [Directorio](https://www.rcastellanos.cdmx.gob.mx/dependencia/directorio)
        
        [Solicitudes administrativas (Historial, constancia...)](https://sites.google.com/rcastellanos.cdmx.gob.mx/deae/inicio)
        
        [Prácticas profesionales](https://sites.google.com/rcastellanos.cdmx.gob.mx/estanciasprofesionales/página-principal)
        
        """
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode="MarkdownV2")