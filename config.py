import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "user_data.db"
CHROMA_PERSIST_DIR = BASE_DIR / "chroma_db"
GUIDES_DIR = BASE_DIR / "guides"

EMBEDDING_MODEL = "D:/HCL/Budgeting Coach/all-MiniLM-L6-v2"

LLM_BACKEND = "cohere"
LLM_MODEL = "command-r-plus-08-2024"   # confirmed working
VISION_MODEL = "c4ai-aya-vision-32b"   # for bill analysis
COHERE_API_KEY = os.getenv("ENTER_YOUR_API_KEY")

CURRENCY_SYMBOL = "₹"
MARKET_CONTEXT = "You are in India. All amounts are in Indian Rupees (₹). Advice should be relevant to the Indian market."