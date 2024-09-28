from pinecone import Pinecone, ServerlessSpec
import os

pinecone = Pinecone(api_key=os.environ.get("PINE_CONE_API_KEY"))
index_name = 'irembo-services-description-v2'

# Ensure index creation happens only once
def ensure_index_exists():
    print(pinecone.list_indexes())
    if pinecone.list_indexes():
        for index in pinecone.list_indexes():
            if index['name'] == index_name:
                break
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=384, spec=ServerlessSpec(cloud="aws", region="us-east-1"))
    return pinecone.Index(index_name)

ensure_index_exists()