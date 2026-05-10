import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 2048
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "success_process.csv")
