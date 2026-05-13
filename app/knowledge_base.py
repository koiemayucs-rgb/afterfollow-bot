import os
import pandas as pd
from functools import lru_cache
from app.config import CSV_PATH

TXT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "recolor_method.txt")


@lru_cache(maxsize=1)
def load_knowledge_base() -> str:
    parts = []

    # ReColorメソッド（テキストファイル）
    if os.path.exists(TXT_PATH):
        with open(TXT_PATH, encoding="utf-8") as f:
            parts.append(f.read())

    # 事例集（CSVファイル）
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        rows = []
        for _, row in df.iterrows():
            cols = [f"{col}: {val}" for col, val in row.items() if pd.notna(val) and str(val).strip()]
            rows.append("\n".join(cols))
        if rows:
            parts.append("## 相談事例集\n\n" + "\n\n---\n\n".join(rows))

    return "\n\n========\n\n".join(parts)
