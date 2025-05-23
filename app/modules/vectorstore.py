import chromadb
from chromadb.utils import embedding_functions

class VectorStore:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.client = chromadb.HttpClient(host=self.host, port=self.port)
        self.default_ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection_documents = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"},
            embedding_function=self.default_ef
        )
        self.collection_feedback = self.client.get_or_create_collection(
            name="feedback",
            metadata={"hnsw:space": "cosine"},
            embedding_function=self.default_ef
        )
    
    def similar_documents(self, text:str, n_results:int=5, where:dict=None):
        text_split = text.split()
        res = self.collection_documents.query(
            query_texts=text_split,
            n_results=n_results,
            where=where,
            include=["documents","distances"]
        )

        return {"documents":res["documents"],"distances":res["distances"]}

    def save_feedback(self, feedback:str, metadata:dict):
        self.collection_feedback.add(
            documents=[feedback],
            embeddings=[self.default_ef([feedback])[0]],
            metadatas=[metadata],
            ids=[str(metadata["id"])]
        )

        print("feedback saved to CrhomaDB")
        return {"feedback":feedback,"metadata":metadata}