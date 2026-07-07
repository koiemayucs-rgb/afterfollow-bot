import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.claude_client import chat_reply

st.set_page_config(
    page_title="Recolor AI サポート",
    page_icon="🌸",
    layout="centered",
)

# ─── スタイル ───────────────────────────────────────────────
st.markdown("""
<style>
/* ページ背景 */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #fff0f4 0%, #fde8f0 100%);
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent; }

/* ヘッダー */
.chat-header {
    background: linear-gradient(135deg, #d63d6e 0%, #e8547a 60%, #f07095 100%);
    border-radius: 20px 20px 0 0;
    padding: 18px 20px 16px;
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 0;
    box-shadow: 0 4px 16px rgba(214,61,110,0.25);
}
.header-icon {
    font-size: 36px;
    background: rgba(255,255,255,0.2);
    border-radius: 50%;
    width: 52px; height: 52px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.header-title {
    color: white;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 0.02em;
}
.header-subtitle {
    color: rgba(255,255,255,0.85);
    font-size: 12px;
    margin-top: 2px;
}
.online-dot {
    width: 10px; height: 10px;
    background: #7effb2;
    border-radius: 50%;
    border: 2px solid white;
    margin-left: auto;
    flex-shrink: 0;
}

/* チャットエリア全体 */
.chat-body {
    background: white;
    border-radius: 0 0 20px 20px;
    padding: 20px 16px 10px;
    min-height: 380px;
    box-shadow: 0 4px 24px rgba(214,61,110,0.10);
}

/* AIメッセージバブル */
.msg-row-ai {
    display: flex;
    align-items: flex-end;
    gap: 8px;
    margin-bottom: 16px;
}
.ai-avatar {
    font-size: 20px;
    background: linear-gradient(135deg, #f9d0dc, #f5b8ca);
    border-radius: 50%;
    width: 36px; height: 36px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 2px 6px rgba(214,61,110,0.15);
}
.bubble-ai {
    background: linear-gradient(135deg, #fff0f4, #fde4ec);
    border: 1px solid #f5c6d8;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 16px;
    max-width: 78%;
    color: #7a2040;
    font-size: 14px;
    line-height: 1.7;
    white-space: pre-wrap;
    box-shadow: 0 2px 8px rgba(214,61,110,0.08);
}

/* ユーザーメッセージバブル */
.msg-row-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 16px;
}
.bubble-user {
    background: linear-gradient(135deg, #e8547a, #d63d6e);
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    max-width: 78%;
    color: white;
    font-size: 14px;
    line-height: 1.7;
    white-space: pre-wrap;
    box-shadow: 0 2px 10px rgba(214,61,110,0.30);
}

/* 日付ラベル */
.date-label {
    text-align: center;
    color: #c4a0b0;
    font-size: 11px;
    margin: 4px 0 18px;
    letter-spacing: 0.05em;
}

/* クイックチップボタン */
.stButton > button {
    background: white !important;
    border: 1.5px solid #f0a8c0 !important;
    border-radius: 20px !important;
    color: #c04070 !important;
    font-size: 12px !important;
    padding: 6px 12px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    white-space: nowrap !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #fde8f0 !important;
    border-color: #d63d6e !important;
    color: #d63d6e !important;
    transform: translateY(-1px);
    box-shadow: 0 3px 8px rgba(214,61,110,0.15) !important;
}

/* チャット入力欄 */
[data-testid="stChatInput"] > div {
    border: 1.5px solid #f0a8c0 !important;
    border-radius: 24px !important;
    background: white !important;
    box-shadow: 0 2px 10px rgba(214,61,110,0.10) !important;
}

/* メインコンテンツの幅調整 */
.block-container {
    max-width: 520px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 1rem !important;
}

/* Streamlitデフォルトのチャットバブルを非表示 */
[data-testid="stChatMessage"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)


# ─── 定数 ─────────────────────────────────────────────────
GREETING = (
    "こんにちは😊 リカラーAIサポートです。\n\n"
    "卒業後のお付き合いで、うれしいことも、ちょっとモヤっとすることも、"
    "どんなことでも気軽に話しかけてみてください。一緒に考えさせていただきますね💕"
)

QUICK_CHIPS = [
    ("🌙 返信が遅くて不安", "返信が遅くて不安です。どうしたらいいですか？"),
    ("📅 会う頻度が減った", "最近会う頻度が減ってきていて心配です"),
    ("💍 結婚を迷っている", "結婚のことで迷っていて、気持ちを整理したいです"),
    ("😶 気持ちが言えない", "自分の気持ちをうまく伝えられなくて困っています"),
]

TODAY = "今日"


# ─── 定数（レート制限） ─────────────────────────────────────
MAX_MESSAGES_PER_SESSION = 20  # 1セッションあたりの最大ユーザー送信数

# ─── セッション初期化 ────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []          # API送信用（挨拶は含まない）
if "display_messages" not in st.session_state:
    st.session_state.display_messages = [   # 表示用（挨拶含む）
        {"role": "assistant", "content": GREETING}
    ]
if "pending_user_input" not in st.session_state:
    st.session_state.pending_user_input = None
if "user_message_count" not in st.session_state:
    st.session_state.user_message_count = 0


# ─── ヘッダー ─────────────────────────────────────────────
st.markdown("""
<div class="chat-header">
    <div class="header-icon">🌸</div>
    <div>
        <div class="header-title">Recolor AI サポート</div>
        <div class="header-subtitle">卒業後もあなたの恋愛に寄り添います</div>
    </div>
    <div class="online-dot"></div>
</div>
""", unsafe_allow_html=True)


# ─── チャット本体（HTMLで描画）────────────────────────────────
chat_html = ['<div class="chat-body">']
chat_html.append(f'<div class="date-label">{TODAY}</div>')

for msg in st.session_state.display_messages:
    content_escaped = (
        msg["content"]
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    if msg["role"] == "assistant":
        chat_html.append(f"""
<div class="msg-row-ai">
    <div class="ai-avatar">🌸</div>
    <div class="bubble-ai">{content_escaped}</div>
</div>""")
    else:
        chat_html.append(f"""
<div class="msg-row-user">
    <div class="bubble-user">{content_escaped}</div>
</div>""")

chat_html.append("</div>")
st.markdown("\n".join(chat_html), unsafe_allow_html=True)


# ─── クイックチップ（最初のユーザー発言前のみ表示）──────────────
user_spoke = any(m["role"] == "user" for m in st.session_state.display_messages)
if not user_spoke:
    col1, col2 = st.columns(2)
    for i, (label, msg_text) in enumerate(QUICK_CHIPS):
        col = col1 if i % 2 == 0 else col2
        if col.button(label, key=f"chip_{i}"):
            st.session_state.pending_user_input = msg_text
            st.rerun()


# ─── レート制限チェック ────────────────────────────────────
def is_rate_limited() -> bool:
    return st.session_state.user_message_count >= MAX_MESSAGES_PER_SESSION


# ─── メッセージ処理 ────────────────────────────────────────
def process_user_message(user_text: str):
    st.session_state.display_messages.append({"role": "user", "content": user_text})
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.session_state.user_message_count += 1

    try:
        reply, _ = chat_reply(st.session_state.messages)
    except Exception as e:
        reply = f"申し訳ありません、エラーが発生しました。もう一度お試しください。\n（{e}）"

    st.session_state.display_messages.append({"role": "assistant", "content": reply})
    st.session_state.messages.append({"role": "assistant", "content": reply})


# チップクリックの処理
if st.session_state.pending_user_input:
    if not is_rate_limited():
        with st.spinner(""):
            process_user_message(st.session_state.pending_user_input)
    st.session_state.pending_user_input = None
    st.rerun()


# ─── テキスト入力 ──────────────────────────────────────────
if is_rate_limited():
    st.markdown("""
    <div style='text-align:center; padding:16px; background:#fff0f4;
                border:1px solid #f5c6d8; border-radius:12px;
                color:#7a2040; font-size:13px; margin-top:8px;'>
        💬 1回のセッションでお話しできるメッセージ数の上限に達しました。<br>
        続きは画面を更新してからまた話しかけてください🌸
    </div>
    """, unsafe_allow_html=True)
else:
    user_input = st.chat_input("気になることを話してみてください…")
    if user_input and user_input.strip():
        with st.spinner(""):
            process_user_message(user_input.strip())
        st.rerun()

# ─── フッター ──────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; margin-top:16px; font-size:11px; color:#c4a0b0;'>
    © 2026 リカラー株式会社 ｜
    <a href='/プライバシーポリシー' target='_self' style='color:#c4a0b0;'>プライバシーポリシー</a> ｜
    <a href='/利用規約' target='_self' style='color:#c4a0b0;'>利用規約・特定商取引法に基づく表示</a>
</div>
""", unsafe_allow_html=True)
