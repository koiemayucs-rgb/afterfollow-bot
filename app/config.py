import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 2048
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "success_process.csv")

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# Streamlit Cloud の Secrets は環境変数より st.secrets 経由で読まれる場合があるため
# db.py 側で直接 st.secrets も参照する
