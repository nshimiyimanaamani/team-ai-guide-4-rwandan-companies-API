# Quicksupport Agent

This project is designed to provide service recommendations for Rwandan companies, utilizing data from Irembo to answer customer inquiries efficiently. The system leverages machine learning models and Pinecone for vector search to deliver accurate and quick responses.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Environment Variables](#environment-variables)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/quicksupport-agent.git
    cd quicksupport-agent
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    ```sh
    export GROQ_API_KEY=your_groq_api_key
    export PINE_CONE_API_KEY=your_pinecone_api_key
    ```

## Usage

1. To start the Flask application:
    ```sh
    python app.py
    ```

2. The application will be available at `http://127.0.0.1:5000`.

## Endpoints

### `POST /recommend`

- **Description**: Recommends a service based on user input.
- **Request Body**:
    ```json
    {
        "user_input": "Describe the service you need"
    }
    ```
- **Response**:
    ```json
    {
        "recommended_service": "Recommended service description"
    }
    ```

## Environment Variables

- `GQ_API_KEY`: API key for Groq.
- `PINE_CONE_API_KEY`: API key for Pinecone.

## Participants

- Nshimiyimana Amani
- Hategekimana Arsene Merci