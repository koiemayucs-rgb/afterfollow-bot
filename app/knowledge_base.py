import pandas as pd
from functools import lru_cache
from app.config import CSV_PATH


@lru_cache(maxsize=1)
def load_knowledge_base() -> str:
    df = pd.read_csv(CSV_PATH)
    rows = []
    for _, row in df.iterrows():
        parts = [f"{col}: {val}" for col, val in row.items() if pd.notna(val) and str(val).strip()]
        rows.append("\n".join(parts))
    return "\n\n---\n\n".join(rows)
