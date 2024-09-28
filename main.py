import requests
import json
import os
import time
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
print(os.environ.get("GROQ_API_KEY"))
pinecone = Pinecone(api_key=os.environ.get("PINE_CONE_API_KEY"))

index_name = 'irembo-services-description-v3'
index = pinecone.Index(index_name)

model = SentenceTransformer('all-MiniLM-L6-v2')

def return_relevant_document_from_pinecone(user_input):
    query_embedding = model.encode(user_input).tolist()
    retries = 3
    for attempt in range(retries):
        try:
            search_response = index.query(
                vector=query_embedding,
                top_k=1,
                include_metadata=True  
            )
            if search_response['matches']:
                relevant_document = search_response['matches'][0]['metadata']['description']
                return relevant_document
            else:
                return "No relevant document found."
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Wait before retrying
    return "Failed to retrieve relevant document after multiple attempts."

user_input = "How to get a passport?"

relevant_document = return_relevant_document_from_pinecone(user_input)

prompt = """
You are a bot that makes recommendations for services. You answer in very short sentences and do not include extra information.
This is the recommended service: {relevant_document}
The user input is: {user_input}
Compile a recommendation to the user based on the recommended service and the user input.
"""

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt.format(user_input=user_input, relevant_document=relevant_document)
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message)
