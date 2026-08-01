import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GST_API_KEY = os.getenv("GST_API_KEY")