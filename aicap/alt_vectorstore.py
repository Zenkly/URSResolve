import hnswlib
from typing import List, Dict
#Vectorstore database
import chromadb
import os

co = chromadb.Client()

class Vectorstore:
    def __init__(self,raw_documents: List[str]):
        self.raw_documents = raw_documents        
        self.docs_embs = []
        self.retrieve_top_k = 10
        self.rerank_top_k = 3        
        self.collection = co.create_collection(name=raw_documents[0]["titulo"].lower().replace(" ","-"))
        self.embed()
        # Chromadb index automatically
        #self.index()

    def embed(self)->None:
        print("Embedding document chunks...")
        documents = []
        metadatas = []
        ids = []
        for i in range(len(self.raw_documents)):
            documents.append(self.raw_documents[i]["seccion"]+ " :: "+ self.raw_documents[i]["contenido"])
            metadatas.append({
                "titulo":self.raw_documents[i]["titulo"],
                "seccion":self.raw_documents[i]["seccion"]
                })
            ids.append("id"+str(i))
        self.collection.add(documents=documents,metadatas=metadatas,ids=ids)


    def retrieve(self,query:str) -> List[Dict[str,str]]:
        query_emb = self.collection.query(
            query_texts=[query],
            n_results=self.rerank_top_k            
        )

        # docs_to_rerank = [self.raw_documents[doc_id]['contenido'] for doc_id in doc_ids]

        # rerank_results = co.rerank(
        #     query=query,
        #     documents=docs_to_rerank,
        #     top_n=self.rerank_top_k,
        #     model="rerank-multilingual-v2.0",
        # )

        # docs_ids_reranked = [doc_ids[result.index] for result in rerank_results.results]

        docs_retrieved=[]
        print(query_emb)
        print(len(query_emb["ids"][0]))
        for i in range(len(query_emb["ids"][0])):
            docs_retrieved.append(
                {             
                    "titulo": query_emb['metadatas'][0][i]["titulo"],
                    "seccion":query_emb['metadatas'][0][i]["seccion"],
                    "contenido":query_emb['documents'][0][i]
                }
            )
        print(docs_retrieved)
        return docs_retrieved