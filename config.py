# config.py
import os

# Fetch the API_KEY and BASE_URL from environment variables
API_KEY = os.getenv("API_KEY", "default_api_key")  # Provide a default if not set
BASE_URL = os.getenv("BASE_URL", "https://default-url.com")  # Provide a default if not set

