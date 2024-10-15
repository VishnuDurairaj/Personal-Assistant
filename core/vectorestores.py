
# ------------------------------------------------- Chroma Vector Store -------------------------------- #

import sys
sys.dont_write_bytecode =True

import os
import hashlib
import chromadb
from chromadb.utils import embedding_functions

os.environ['ALLOW_RESET']='TRUE'

class ChromaDB:
    def __init__(self,store_id="my_data", collection_name="documents", embedding_model_name="all-MiniLM-L6-v2"):
        """
        Initialize the vector store using SentenceTransformer for embeddings.

        :param collection_name: Name of the collection to store documents.
        :param embedding_model_name: SentenceTransformer model name to use for embeddings.
        """
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(f"chroma_db/{store_id}") 

        # Initialize the SentenceTransformer model for embeddings
        self.embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embedding_model_name)


        # Create or load collection, providing a custom embedding function
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_model
        )

    def add_documents(self, documents:list):
        """
        Add documents to the vector store.
        
        :param documents: List of documents to add.
        :param ids: List of unique IDs for each document.
        """

        ids = [self.generate_short_unique_id(i) for i  in documents]
               
        if len(documents) != len(ids):
            raise ValueError("Documents and IDs must have the same length.")
        
        # Embed the documents using the SentenceTransformer model
        self.collection.add(documents=documents, ids=ids)
        return f"Added {len(documents)} documents."

    def retrieve_top_n(self, query, n=5):
        """
        Retrieve the top N most similar documents to the query.
        
        :param query: The query document.
        :param n: Number of top documents to retrieve.
        :return: List of top N documents.
        """
        # Embed the query document
        query_embedding = self.embedding_model([query])
        
        # Perform the query on the collection to retrieve top N results
        results = self.collection.query(query_embeddings=query_embedding, n_results=n)
        return results

    def delete_document(self, doc_id):
        """
        Delete a document by its ID.
        
        :param doc_id: ID of the document to delete.
        """
        self.collection.delete(ids=[doc_id])
        return f"Document with ID {doc_id} deleted."

    def update_document(self, doc_id, new_document):
        """
        Update an existing document by its ID.
        
        :param doc_id: ID of the document to update.
        :param new_document: The new content for the document.
        """
        # First delete the old document, then add the new one with the same ID.
        self.delete_document(doc_id)
        self.add_documents([new_document])
        return f"Document with ID {doc_id} updated."

    def reset(self):

        self.client.reset()

        return "Deleted Existing Data....."
    
    def generate_short_unique_id(self,text, length=8):
        """
        Generate a short unique ID based on the given text using SHA-256 hashing.
        
        :param text: Input text to generate the unique ID from.
        :param length: Length of the unique ID (default is 8 characters).
        :return: A short unique ID string.
        """
        # Generate SHA-256 hash of the text
        hash_object = hashlib.sha256(text.encode('utf-8'))
        
        # Convert the hash to a hexadecimal string and truncate to desired length
        unique_id = hash_object.hexdigest()[:length]
        
        return unique_id


# ------------------------------------------------- Qdrant Vector Store -------------------------------- #

# Import client library
# from qdrant_client import QdrantClient
# from tqdm import tqdm

# class QdrantVectorStore:
#     def __init__(self,db_location="qdrant",dense_model="sentence-transformers/all-MiniLM-L6-v2",sparse_model = "prithivida/Splade_PP_en_v1",hybird=True) -> None:
        
#         self.client = QdrantClient(path=f"vector_stores/{db_location}")

#         self.client.set_model(dense_model)
#         # comment this line to use dense vectors only
#         if hybird:
#             self.client.set_sparse_model(sparse_model)

#             self.client.recreate_collection(
#                 collection_name="schema_details",
#                 vectors_config=self.client.get_fastembed_vector_params(),
#                 # comment this line to use dense vectors only
#                 sparse_vectors_config=self.client.get_fastembed_sparse_vector_params(),  
#             )
#         else:

#             self.client.recreate_collection(
#                 collection_name="schema_details",
#                 vectors_config=self.client.get_fastembed_vector_params()
#             )

#     def add_documents_to_schema_details(self,documents,ids,collection_name="schema_details"):
#         self.client.add(
#         collection_name=collection_name,
#         documents=documents,
#         ids=tqdm(ids))

#     def get_relavant_documents(self, text: str,collection_name:str="schema_details",top_n_similar_docs=6):
#         search_result = self.client.query(
#             collection_name=collection_name,
#             query_text=text,
#             limit=top_n_similar_docs, 
#         )
#         metadata = [{"id":hit.id,"document":hit.metadata['document']} for hit in search_result]
#         return metadata
    
    