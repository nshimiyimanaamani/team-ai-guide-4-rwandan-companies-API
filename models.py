import warnings

# Suppress the FutureWarning related to clean_up_tokenization_spaces
warnings.filterwarnings("ignore", category=FutureWarning)

from sentence_transformers import SentenceTransformer

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')
