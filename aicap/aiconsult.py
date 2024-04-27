import cohere
#from aicap.vectorstore import Vectorstore
from aicap.alt_vectorstore import Vectorstore
from chats_db.history import historyDB
from openai import OpenAI
import os

cohere_token = os.getenv('COHERE_TOKEN')
co = cohere.Client(cohere_token)

client = OpenAI()



class AiConsult:
    def __init__(self,vectorstore: Vectorstore, preamble: str):

        self.vectorstore = vectorstore                       
        self.preamble = preamble         
        self.chat_history = []
        self.current_conversation = []
        historyDB.crear_tablas_si_no_existen()

          
    
    def consult(self,user,input_message):        
        self.chat_history=historyDB.obtener_historial(user)
        message = input_message
        # preamble ="""
        # ### Context
        # Eres un chatbot inteligente, de nombre URCSolve de la Universidad Rosario Castellanos (URC). Siempre debes contestar en español.
        # Siempre eres amable y políticamente correcto. Contestas basado siempre en el contexto. A menos que se indique lo contrario, tus respuestas priorizan información sobre casos de licenciatura.
        # Si la respuesta no está contenida explicitamente en los documentos respondes educadamente que no conoces la respuesta. If documents do not contains answer, then reply "No conozco la respuesta a tu pregunta".
        # """
        preamble ="""
        ### Context:

        """
        preamble = preamble + self.preamble + "\n"
        
        print("preamble:")
        print(preamble)

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

        #print("\nChatbot:")
        citations = response.citations
        cited_documents = response.documents

        answer = response.text

        # if citations:
        #     print("\n\nCITATIONS:")
        #     for citation in citations:
        #         print(citation)

        #     print("\nDOCUMENTS:")
        #     for document in cited_documents:
        #         print(document)

        user_message = {"role": "USER", "text":message}      
        bot_message = {"role": "CHATBOT", "text": answer}  
        self.current_conversation.append(user_message)
        self.current_conversation.append(bot_message)
        historyDB.guardar_arreglo(user,self.current_conversation)
        
        #print(answer, end="")
        return answer
    
    def query_OpenAillm(system_message,prompt, history,model="gpt-3.5-turbo"):
        #print("Querying...")
        history.insert(0,{"role": "system", "content": system_message})
        history.append({"role": "user", "content": prompt})
        #print(history)
        completions = client.chat.completions.create(        
        model="gpt-3.5-turbo",
            messages=history,
            temperature=0.0,
        )
        #print("Finish...")
        #print(completions.choices[0].message.content)
        return completions.choices[0].message.content

    def consultOpenAi(self,user,input_message):        
        self.chat_history=historyDB.obtener_historial(user,openAi=True)
        message = input_message
        # preamble ="""
        # ### Context
        # Eres un chatbot inteligente, de nombre URCSolve de la Universidad Rosario Castellanos (URC). Siempre debes contestar en español.
        # Siempre eres amable y políticamente correcto. Contestas basado siempre en el contexto. A menos que se indique lo contrario, tus respuestas priorizan información sobre casos de licenciatura.
        # Si la respuesta no está contenida explicitamente en los documentos respondes educadamente que no conoces la respuesta. If documents do not contains answer, then reply "No conozco la respuesta a tu pregunta".
        # """
        template_rag =self.preamble + """
        
        Contexto:
        ```
        {context}
        ```
        """
        if message == "":
            return "Estoy aquí para ayudarte"
                            
        else:
            print(f"User: {message}")


        #print("Recuperando información...", end="")            

        documents=self.vectorstore.retrieve(input_message)

        context = ""

        for doc in documents:
            context_n = doc["titulo"] +": " + doc["seccion"] +": " +doc["contenido"]
            context = context + "\n" + context_n
            print(doc)
        

        final_prompt = template_rag.format(context=context)
        #print(type(final_prompt))
        #print("Querying...")        
        #print(self.chat_history)
        answer = AiConsult.query_OpenAillm(final_prompt,input_message,self.chat_history)

        user_message = {"role": "USER", "text":message}      
        bot_message = {"role": "CHATBOT", "text": answer}  
        self.current_conversation.append(user_message)
        self.current_conversation.append(bot_message)
        historyDB.guardar_arreglo(user,self.current_conversation)
        
        return answer