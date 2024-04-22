import cohere
from aicap.vectorstore import Vectorstore
from chats_db.history import historyDB
import os

cohere_token = os.getenv('COHERE_TOKEN')
co = cohere.Client(cohere_token)

class AiConsult:
    def __init__(self,vectorstore: Vectorstore):

        self.vectorstore = vectorstore                                
        self.chat_history = []
        self.current_conversation = []
        historyDB.crear_tabla_si_no_existe()

          
    
    def consult(self,user,input_message):        
        self.chat_history=historyDB.obtener_historial(user)
        message = input_message
        preamble ="""
        ### Context
        Eres un chatbot inteligente, de nombre URCSolve de la Universidad Rosario Castellanos (URC). Siempre debes contestar en español.
        Siempre eres amable y políticamente correcto. Contestas basado siempre en el contexto. A menos que se indique lo contrario, tus respuestas priorizan información sobre casos de licenciatura.
        Si la respuesta no está contenida explicitamente en los documentos respondes educadamente que no conoces la respuesta. If documents do not contains answer, then reply "No conozco la respuesta a tu pregunta".
        """
        if message == "":
            return "Estoy aquí para ayudarte"
                               
        else:
            print(f"User: {message}")

        response = co.chat(message=message, search_queries_only=True)

        if response.search_queries:
            print("Recuperando información...", end="")

            documents = []

            for query in response.search_queries:
                documents.extend(self.vectorstore.retrieve(query.text))

            response = co.chat(
                message=message,
                model = "command-r",
                documents=documents,
                preamble=preamble,
                temperature=0.0,
                #conversation_id=self.conversation_id
                chat_history=self.chat_history
            )

        else:
            response = co.chat(
                message=message,
                model="command-r",
                preamble=preamble,
                temperature=0.0,
                #conversation_id=self.conversation_id
                chat_history=self.chat_history
            )

        print("\nChatbot:")
        citations = response.citations
        cited_documents = response.documents

        answer = response.text

        if citations:
            print("\n\nCITATIONS:")
            for citation in citations:
                print(citation)

            print("\nDOCUMENTS:")
            for document in cited_documents:
                print(document)

        user_message = {"role": "USER", "text":message}      
        bot_message = {"role": "CHATBOT", "text": answer}  
        self.current_conversation.append(user_message)
        self.current_conversation.append(bot_message)
        historyDB.guardar_arreglo(user,self.current_conversation)
        
        print(answer, end="")
        return answer
