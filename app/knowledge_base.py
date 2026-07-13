import os
import pandas as pd
from functools import lru_cache
from app.config import CSV_PATH

TXT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "recolor_method.txt")
SRANK_TXT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "srank_mindset.txt")
CLIENT_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "client_data.csv")
SEX_FAQ_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sex_relationship_faq.txt")


def _summarize_client_data() -> str:
    """生徒データCSVを集計してサマリーテキストを生成する"""
    if not os.path.exists(CLIENT_DATA_PATH):
        return ""

    df = pd.read_csv(CLIENT_DATA_PATH)

    # 成就有無の列
    success_col = "生徒からの成就報告"
    phase_col = "現在フェーズ"
    class_col = "生徒分類"

    if success_col not in df.columns:
        return ""

    df["成就"] = df[success_col].astype(str).str.upper() == "TRUE"
    total = len(df)
    succeeded = df["成就"].sum()
    success_rate = succeeded / total * 100 if total > 0 else 0

    lines = [
        "## 生徒データ集計（成就傾向サマリー）",
        f"- 総生徒数: {total}名",
        f"- 成就数: {int(succeeded)}名（成就率: {success_rate:.1f}%）",
        "",
    ]

    # フェーズ別の成就率
    if phase_col in df.columns:
        lines.append("### フェーズ別 成就率")
        phase_stats = df.groupby(phase_col)["成就"].agg(["sum", "count"])
        phase_stats["成就率"] = (phase_stats["sum"] / phase_stats["count"] * 100).round(1)
        phase_order = [
            "フェーズ0：マッチング",
            "フェーズ1：初回デート",
            "フェーズ2：関係構築",
            "フェーズ3：関係深化",
            "フェーズ4：意思決定",
            "フェーズ5：成就間際",
            "未設定",
        ]
        for phase in phase_order:
            if phase in phase_stats.index:
                row = phase_stats.loc[phase]
                lines.append(f"- {phase}: {int(row['sum'])}/{int(row['count'])}名 （{row['成就率']}%）")
        lines.append("")

    # 生徒分類別の成就率
    if class_col in df.columns:
        lines.append("### 生徒分類別 成就率")
        valid = df[df[class_col].notna() & (df[class_col].str.strip() != "")]
        class_stats = valid.groupby(class_col)["成就"].agg(["sum", "count"])
        class_stats["成就率"] = (class_stats["sum"] / class_stats["count"] * 100).round(1)
        class_stats = class_stats.sort_values("成就率", ascending=False)
        for cls, row in class_stats.iterrows():
            short = cls.split("（")[0].strip()  # 括弧内の長い説明を省略
            lines.append(f"- {short}: {int(row['sum'])}/{int(row['count'])}名 （{row['成就率']}%）")
        lines.append("")

    # 成就した人の特徴
    succeeded_df = df[df["成就"]]
    lines.append("### 成就した生徒の特徴")
    if "半日デート" in df.columns:
        half_day = succeeded_df["半日デート"].value_counts().to_dict()
        lines.append(f"- 半日デート状況: {half_day}")
    if "相手からの好意" in df.columns:
        affection = succeeded_df["相手からの好意"].value_counts().to_dict()
        lines.append(f"- 相手からの好意: {affection}")
    if "交際意思の言質" in df.columns:
        intent = succeeded_df["交際意思の言質"].value_counts().to_dict()
        lines.append(f"- 交際意思: {intent}")

    return "\n".join(lines)


@lru_cache(maxsize=1)
def load_knowledge_base() -> str:
    parts = []

    # ReColorメソッド（テキストファイル）
    if os.path.exists(TXT_PATH):
        with open(TXT_PATH, encoding="utf-8") as f:
            parts.append(f.read())

    # Sランク育成研修：マインド分析・インナーチャイルド理解
    if os.path.exists(SRANK_TXT_PATH):
        with open(SRANK_TXT_PATH, encoding="utf-8") as f:
            parts.append(f.read())

    # 生徒データ集計サマリー
    client_summary = _summarize_client_data()
    if client_summary:
        parts.append(client_summary)

    # セックス・パートナーシップ Q&A
    if os.path.exists(SEX_FAQ_PATH):
        with open(SEX_FAQ_PATH, encoding="utf-8") as f:
            parts.append(f.read())

    # 相談事例集（CSVファイル）
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        rows = []
        for _, row in df.iterrows():
            cols = [f"{col}: {val}" for col, val in row.items() if pd.notna(val) and str(val).strip()]
            rows.append("\n".join(cols))
        if rows:
            parts.append("## 相談事例集\n\n" + "\n\n---\n\n".join(rows))

    return "\n\n========\n\n".join(parts)
