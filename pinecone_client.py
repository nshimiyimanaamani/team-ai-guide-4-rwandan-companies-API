import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

pinecone = Pinecone(api_key=os.environ.get("PINE_CONE_API_KEY"))

index_name = 'irembo-services-description-v2'
index = pinecone.Index(index_name)

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_service_recommendation(user_input):
    def return_relevant_document_from_pinecone(user_input):
        query_embedding = model.encode(user_input).tolist()

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

    relevant_document = return_relevant_document_from_pinecone(user_input)

    prompt = """
    You are an AI Service Guide for Rwandan companies, designed to streamline customer service for platforms like Irembo and MTN. 
    Currently, you are utilizing data from Irembo to answer customer inquiries efficiently. 
    Your goal is to provide quick and accurate responses, reducing reliance on human agents. 
    This is the recommended service: {relevant_document}
    The user input is: {user_input}
    Based on the recommended service and the user's question, provide a concise and helpful recommendation that informs the customer while ensuring efficiency in service delivery.
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

    return chat_completion.choices[0].message.content.replace('\n', ' ').replace('\\', '').strip()
