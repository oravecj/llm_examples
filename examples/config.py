import os
import urllib3
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_KEY = os.environ.get("OPENAI_API_KEY")
API_URL = os.environ.get("API_URL") or "https://api.openai.com/v1/chat/completions"

# Suppress warnings about self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
