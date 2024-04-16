
import cohere
import hnswlib
from typing import List, Dict
import os

cohere_token = os.getenv('COHERE_TOKEN')
co = cohere.Client(cohere_token)

class Vectorstore:
    def __init__(self,raw_documents: List[str]):
        self.raw_documents = raw_documents        
        self.docs_embs = []
        self.retrieve_top_k = 10
        self.rerank_top_k = 3
        self.embed()
        self.index()

    def embed(self)->None:
        print("Embedding document chunks...")

        batch_size = 90
        self.docs_len = len(self.raw_documents)
        for i in range(0,self.docs_len,batch_size):
            batch = self.raw_documents[i:min(i+batch_size,self.docs_len)]
            texts = [item["seccion"]+ " :: "+ item["contenido"] for item in batch]
            docs_embs_batch = co.embed(
            texts = texts, model="embed-multilingual-v3.0",input_type="search_document"
            ).embeddings
            self.docs_embs.extend(docs_embs_batch)

    def index(self) -> None:
        print("Indexing documents...")
        
        self.idx = hnswlib.Index(space="ip",dim=1024)
        self.idx.init_index(max_elements=self.docs_len,ef_construction = 512,M=64)
        self.idx.add_items(self.docs_embs,list(range(len(self.docs_embs))))

        print(f"Indexing complete with {self.idx.get_current_count()} documents.")


    def retrieve(self,query:str) -> List[Dict[str,str]]:
        query_emb = co.embed(
            texts=[query], model="embed-multilingual-v3.0", input_type="search_query"
        ).embeddings

        doc_ids = self.idx.knn_query(query_emb, k=self.rerank_top_k)[0][0]

        docs_to_rerank = [self.raw_documents[doc_id]['contenido'] for doc_id in doc_ids]

        rerank_results = co.rerank(
            query=query,
            documents=docs_to_rerank,
            top_n=self.rerank_top_k,
            model="rerank-multilingual-v2.0",
        )

        docs_ids_reranked = [doc_ids[result.index] for result in rerank_results.results]

        docs_retrieved=[]
        for doc_id in docs_ids_reranked:
            docs_retrieved.append(
                {             
                    "titulo": self.raw_documents[doc_id]["titulo"],
                    "seccion":self.raw_documents[doc_id]["seccion"],
                    "contenido":self.raw_documents[doc_id]["contenido"]
                }
            )

        return docs_retrieved