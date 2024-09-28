import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from groq import Groq

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Initialize Pinecone client
pinecone = Pinecone(api_key=os.environ.get("PINE_CONE_API_KEY"))

# Specify the index name
index_name = 'irembo-services-description-v2'
index = pinecone.Index(index_name)

# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_service_recommendation(user_input):
    # Function to retrieve relevant document from Pinecone
    def return_relevant_document_from_pinecone(user_input):
        # Encode the user query to get the embedding
        query_embedding = model.encode(user_input).tolist()

        # Query Pinecone for the most relevant document
        search_response = index.query(
            vector=query_embedding, 
            top_k=1, 
            include_metadata=True  
        )

        # Check for matches and return the relevant document
        if search_response['matches']:
            relevant_document = search_response['matches'][0]['metadata']['description']
            return relevant_document
        else:
            return "No relevant document found."

    # Retrieve the relevant document from Pinecone
    relevant_document = return_relevant_document_from_pinecone(user_input)

    # Prepare the prompt for Groq
    prompt = """
    You are an AI Service Guide for Rwandan companies, designed to streamline customer service for platforms like Irembo and MTN. 
    Currently, you are utilizing data from Irembo to answer customer inquiries efficiently. 
    Your goal is to provide quick and accurate responses, reducing reliance on human agents. 
    This is the recommended service: {relevant_document}
    The user input is: {user_input}
    Based on the recommended service and the user's question, provide a concise and helpful recommendation that informs the customer while ensuring efficiency in service delivery.
    """

    # Generate the chat completion using Groq
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt.format(user_input=user_input, relevant_document=relevant_document)
            }
        ],
        model="llama3-8b-8192",
    )

    # Return the generated recommendation without newline characters
    return chat_completion.choices[0].message.content.replace('\n', ' ').strip()
