import requests
import json
import os
import uuid
from pinecone import Pinecone, ServerlessSpec
from models import model

pinecone = Pinecone(api_key=os.environ.get("PINE_CONE_API_KEY"))
index_name = 'irembo-services-description-v2'

def ensure_index_exists():
    existing_indexes = pinecone.list_indexes()

    if any(index['name'] == index_name for index in existing_indexes):
        print(f"Index '{index_name}' already exists.")
    else:
        pinecone.create_index(index_name, dimension=384, spec=ServerlessSpec(cloud="aws", region="us-east-1"))
        print(f"Created new index '{index_name}'.")

    return pinecone.Index(index_name)

# Load services from the JSON file and process them
def process_services():
    with open('services.json', 'r') as file:
        services = json.load(file)

    service_dict = {}
    for data in services['data']:
        if data['groupedServiceList']:
            for groupedService in data['groupedServiceList']:
                service_dict[groupedService['code']] = groupedService['name']

    results = []
    for code in service_dict.keys():
        api_response = fetch_data_from_api(code)
        if api_response and 'data' in api_response:
            for response in api_response['data']:
                if response.get('description') and response['owner']:
                    price = response['basePrice']
                    currency = response['currency']['name']
                    owner = response['owner']['name']

                    full_description = f"{response['description']} by {owner} for {price} {currency}. It takes about {response['processingDays']} days. This service can be applied for via Irembo (https://irembo.gov.rw)."
                    
                    result = {
                        'code': code,
                        'name': service_dict[code],
                        'description': full_description
                    }
                    results.append(result)

    save_service_results(results)
    upsert_services_to_pinecone(results)

# Fetch data from the Irembo API
def fetch_data_from_api(code):
    url = 'https://irembo.gov.rw/irembo/rest/public/service/group'
    headers = {
        'groupcode': code,
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0',
        'nls': 'English'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Save the updated service results to a JSON file
def save_service_results(results):
    with open('service_results.json', 'w') as outfile:
        json.dump(results, outfile, indent=4)


def upsert_services_to_pinecone(results):
    index = ensure_index_exists() 
    
    for service in results:
        description = service['description']
        embedding = model.encode(description).tolist()
        unique_id = str(uuid.uuid4())
        
        index.upsert([{
            'id': unique_id,
            'values': embedding,
            'metadata': {
                'description': description
            }
        }])

def get_relevant_document(query):
    from pinecone_client import get_service_recommendation
    return get_service_recommendation(query)
