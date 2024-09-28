import warnings
from sentence_transformers import SentenceTransformer

warnings.filterwarnings("ignore", category=FutureWarning)
model = SentenceTransformer('all-MiniLM-L6-v2')
