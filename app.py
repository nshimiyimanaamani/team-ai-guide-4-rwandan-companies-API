from flask import Flask, request, jsonify
from services import get_relevant_document, process_services
import os

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend_service():
    user_input = request.json.get('user_input', '')
    relevant_document = get_relevant_document(user_input)
    
    if relevant_document == "No relevant document found.":
        return jsonify({'error': relevant_document}), 404

    return jsonify({'recommended_service': relevant_document})

if __name__ == '__main__':
    process_services()
    app.run(debug=True)
