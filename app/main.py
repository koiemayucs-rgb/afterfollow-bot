import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.claude_client import chat_reply
from app.db import load_history, save_message, has_consented, save_consent, CONSENT_VERSION

st.set_page_config(
    page_title="ReColor AI サポート",
    page_icon="🌸",
    layout="centered",
)


def _chat_page():
    MAX_MESSAGES_PER_SESSION = 20

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

    # ─── 認証ゲート ────────────────────────────────────────────
    if not st.user.is_logged_in:
        st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(160deg, #fff0f4 0%, #fde8f0 100%);
            min-height: 100vh;
        }
        [data-testid="stHeader"] { background: transparent; }
        .block-container { max-width: 480px !important; padding-top: 4rem !important; }
        .login-card {
            background: white;
            border-radius: 24px;
            padding: 40px 32px 32px;
            box-shadow: 0 8px 32px rgba(214,61,110,0.15);
            text-align: center;
        }
        .login-icon { font-size: 64px; margin-bottom: 12px; }
        .login-title {
            color: #d63d6e;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 6px;
        }
        .login-sub {
            color: #9a6070;
            font-size: 13px;
            line-height: 1.7;
            margin-bottom: 28px;
        }
        .stButton > button {
            background: linear-gradient(135deg, #d63d6e, #e8547a) !important;
            color: white !important;
            border: none !important;
            border-radius: 24px !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
            width: 100% !important;
            box-shadow: 0 4px 14px rgba(214,61,110,0.35) !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="login-card">
            <div class="login-icon">🌸</div>
            <div class="login-title">ReColor AI サポート</div>
            <div class="login-sub">
                卒業後のお付き合いに寄り添う、<br>
                リカラー専用の AI 相談チャットです。<br><br>
                Googleアカウントでログインしてご利用ください。
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            if st.button("🔑 Googleアカウントでログイン", use_container_width=True):
                st.login("google")

        st.markdown("""
        <div style='text-align:center; margin-top:24px; font-size:11px; color:#c4a0b0;'>
            © 2026 株式会社リカラー ｜
            <a href='/プライバシーポリシー' target='_self' style='color:#c4a0b0;'>プライバシーポリシー</a> ｜
            <a href='/利用規約' target='_self' style='color:#c4a0b0;'>利用規約</a>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # ─── 同意ゲート ────────────────────────────────────────────
    _user_email_early = st.user.email or ""

    if "consent_verified" not in st.session_state:
        st.session_state.consent_verified = has_consented(_user_email_early, CONSENT_VERSION)

    if not st.session_state.consent_verified:
        st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(160deg, #fff0f4 0%, #fde8f0 100%);
            min-height: 100vh;
        }
        [data-testid="stHeader"] { background: transparent; }
        .block-container { max-width: 640px !important; padding-top: 2.5rem !important; }
        .consent-card {
            background: white;
            border-radius: 20px;
            padding: 32px 28px 24px;
            box-shadow: 0 8px 32px rgba(214,61,110,0.15);
        }
        .consent-title {
            color: #d63d6e;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 16px;
            text-align: center;
        }
        .consent-body {
            color: #5a3040;
            font-size: 13.5px;
            line-height: 1.8;
        }
        .consent-warn {
            background: #f0f6ff;
            border-left: 3px solid #6090d0;
            padding: 10px 14px;
            border-radius: 4px;
            margin: 14px 0;
            font-size: 12.5px;
            color: #304060;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="consent-card">
            <div class="consent-title">🌸 ご利用前にご確認ください</div>
            <div class="consent-body">
                本サービスは、以下の米国にある事業者と連携してサービスを提供しています。
                <br><br>
                <b>・Anthropic, Inc.（米国）</b><br>
                　会話テキストをもとに、AIが返答を生成します。<br>
                　取得したデータはモデルの学習には使用されません。<br><br>
                <b>・Supabase, Inc.（米国）</b><br>
                　会話履歴を安全に保存・管理します。<br>
                　データの保存先は東京リージョン（日本国内）です。
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="consent-warn">
            ℹ️ Anthropic・Supabase はいずれも米国の企業です。米国には日本の個人情報保護法に相当する包括的な連邦法がないため、データの取り扱いが日本と異なる場合があります。詳細は「外国にある事業者への情報の提供について」をご確認いただけます。
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            "詳細：[外国にある事業者への情報の提供について](/外国にある事業者への情報の提供について)"
            "　｜　[プライバシーポリシー](/プライバシーポリシー)",
            unsafe_allow_html=False,
        )

        agreed = st.checkbox(
            "上記およびプライバシーポリシー・外国にある事業者への情報の提供についてを確認し、"
            "外国にある事業者への情報の提供に同意します",
            key="consent_checkbox",
        )

        col1, col2 = st.columns(2)
        if col1.button("同意して利用を開始する", use_container_width=True, type="primary"):
            if agreed:
                save_consent(_user_email_early, CONSENT_VERSION)
                st.session_state.consent_verified = True
                st.rerun()
            else:
                st.error("チェックボックスにチェックを入れてから進んでください。")

        if col2.button("同意しない", use_container_width=True):
            st.logout()

        st.markdown(
            "<div style='text-align:center; margin-top:20px; font-size:11px; color:#c4a0b0;'>"
            "同意しない場合は本サービスをご利用いただけません。<br>"
            "退会・同意の撤回は info@recolor-inc.net までご連絡ください。</div>",
            unsafe_allow_html=True,
        )
        st.stop()

    # ─── スタイル ───────────────────────────────────────────────
    st.markdown("""
<style>
/* ダークモード無効化：システムの配色設定に関わらず常にライトモードで表示 */
:root, html, body {
    color-scheme: light !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #fff0f4 0%, #fde8f0 100%);
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent; }

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

.chat-body {
    background: white;
    border-radius: 0 0 20px 20px;
    padding: 20px 16px 10px;
    min-height: 380px;
    box-shadow: 0 4px 24px rgba(214,61,110,0.10);
}

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

.date-label {
    text-align: center;
    color: #c4a0b0;
    font-size: 11px;
    margin: 4px 0 18px;
    letter-spacing: 0.05em;
}

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

[data-testid="stChatInput"] > div {
    border: 1.5px solid #f0a8c0 !important;
    border-radius: 24px !important;
    background: white !important;
    box-shadow: 0 2px 10px rgba(214,61,110,0.10) !important;
}
[data-testid="stChatInput"] textarea {
    color: #333333 !important;
    background: white !important;
    caret-color: #d63d6e !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #c4a0b0 !important;
}

.block-container {
    max-width: 520px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 1rem !important;
}

[data-testid="stChatMessage"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

    # ─── セッション初期化（過去履歴をロード）────────────────────────
    _user_email = _user_email_early

    if "history_loaded" not in st.session_state:
        past = load_history(_user_email)
        st.session_state.messages = past
        if past:
            st.session_state.display_messages = list(past)
        else:
            st.session_state.display_messages = [
                {"role": "assistant", "content": GREETING}
            ]
        st.session_state.history_loaded = True

    if "pending_user_input" not in st.session_state:
        st.session_state.pending_user_input = None
    if "user_message_count" not in st.session_state:
        st.session_state.user_message_count = 0

    # ─── ユーザーバー（ログアウト） ──────────────────────────────
    _user_name = st.user.name or st.user.email or "ゲスト"
    _col_name, _col_logout = st.columns([4, 1])
    _col_name.markdown(
        f"<div style='font-size:12px; color:#c4a0b0; padding-top:6px;'>👤 {_user_name}</div>",
        unsafe_allow_html=True,
    )
    if _col_logout.button("ログアウト", key="_logout"):
        st.logout()

    # ─── ヘッダー ─────────────────────────────────────────────
    st.markdown("""
<div class="chat-header">
    <div class="header-icon">🌸</div>
    <div>
        <div class="header-title">ReColor AI サポート</div>
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
        save_message(_user_email, "user", user_text)

        try:
            reply, _ = chat_reply(st.session_state.messages)
        except Exception as e:
            reply = f"申し訳ありません、エラーが発生しました。もう一度お試しください。\n（{e}）"

        st.session_state.display_messages.append({"role": "assistant", "content": reply})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        save_message(_user_email, "assistant", reply)

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
    © 2026 株式会社リカラー ｜
    <a href='/プライバシーポリシー' target='_self' style='color:#c4a0b0;'>プライバシーポリシー</a> ｜
    <a href='/利用規約' target='_self' style='color:#c4a0b0;'>利用規約</a> ｜
    <a href='/特定商取引法に基づく表示' target='_self' style='color:#c4a0b0;'>特定商取引法に基づく表示</a>
</div>
""", unsafe_allow_html=True)


# ─── ナビゲーション定義（サイドバーに表示するページを制御）──────────
pg = st.navigation(
    [
        st.Page(_chat_page, default=True, url_path=""),
        st.Page("pages/1_プライバシーポリシー.py", title="プライバシーポリシー"),
        st.Page("pages/2_利用規約.py", title="利用規約"),
        st.Page("pages/3_特定商取引法に基づく表示.py", title="特定商取引法に基づく表示"),
        st.Page(
            "pages/_外国にある事業者への情報の提供について.py",
            title="外国にある事業者への情報の提供について",
        ),
    ],
    position="hidden",  # 自動生成ナビを非表示にして手動で制御
)

# サイドバーに表示したい3ページだけを手動で追加
st.sidebar.page_link("pages/1_プライバシーポリシー.py", label="プライバシーポリシー")
st.sidebar.page_link("pages/2_利用規約.py", label="利用規約")
st.sidebar.page_link("pages/3_特定商取引法に基づく表示.py", label="特定商取引法に基づく表示")

# GitHubソースコードリンクボタンを非表示
st.markdown("""
<style>
[data-testid="stHeader"] a[href*="github"] { display: none !important; }
[data-testid="stToolbar"] a[href*="github"] { display: none !important; }
header a[href*="github"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

pg.run()
