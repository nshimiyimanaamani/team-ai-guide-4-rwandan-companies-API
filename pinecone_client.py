from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import os

pinecone = Pinecone(api_key=os.environ.get("PINE_CONE_API_KEY"))
index_name = 'irembo-services-description-v2'
index = pinecone.Index(index_name)
model = SentenceTransformer('all-MiniLM-L6-v2')

def return_relevant_document_from_pinecone(query):
    query_embedding = model.encode(query).tolist()
    search_response = index.query(vector=query_embedding, top_k=1, include_metadata=True)
    
    if search_response['matches']:
        relevant_document = search_response['matches'][0]['metadata']['description']
        return relevant_document
    else:
        return "No relevant document found."
