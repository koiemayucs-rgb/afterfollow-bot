import streamlit as st
from supabase import create_client, Client

CONSENT_VERSION = "1.0"


def _get_config() -> tuple[str, str]:
    """Streamlit Secrets → 環境変数の順で URL と Key を取得する。"""
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
    except Exception:
        from app.config import SUPABASE_URL, SUPABASE_KEY
        url, key = SUPABASE_URL, SUPABASE_KEY
    return url, key

HISTORY_LIMIT = 100  # 1ユーザーあたりロードする最大メッセージ数


@st.cache_resource
def _get_client() -> Client:
    url, key = _get_config()
    return create_client(url, key)


def save_message(user_email: str, role: str, content: str) -> None:
    """会話の1メッセージをSupabaseに保存する。"""
    url, key = _get_config()
    if not url or not key:
        return
    try:
        _get_client().table("conversations").insert({
            "user_email": user_email,
            "role": role,
            "content": content,
        }).execute()
    except Exception:
        pass  # 保存失敗してもチャットは続行させる


def load_history(user_email: str) -> list[dict]:
    """ユーザーの過去会話を古い順で返す（最大HISTORY_LIMIT件）。"""
    url, key = _get_config()
    if not url or not key:
        return []
    try:
        res = (
            _get_client()
            .table("conversations")
            .select("role, content, created_at")
            .eq("user_email", user_email)
            .order("created_at", desc=True)
            .limit(HISTORY_LIMIT)
            .execute()
        )
        rows = res.data or []
        # 新着順→古い順に並べ替えて返す
        rows.reverse()
        return [{"role": r["role"], "content": r["content"]} for r in rows]
    except Exception:
        return []


def has_consented(user_email: str, version: str = CONSENT_VERSION) -> bool:
    """指定バージョンへの同意済みかどうかを確認する。"""
    url, key = _get_config()
    if not url or not key:
        return False
    try:
        res = (
            _get_client()
            .table("consents")
            .select("id")
            .eq("user_email", user_email)
            .eq("consent_version", version)
            .limit(1)
            .execute()
        )
        return len(res.data) > 0
    except Exception:
        return False


def save_consent(user_email: str, version: str = CONSENT_VERSION) -> None:
    """ユーザーの同意記録をSupabaseに保存する。"""
    url, key = _get_config()
    if not url or not key:
        return
    try:
        _get_client().table("consents").upsert(
            {"user_email": user_email, "consent_version": version},
            on_conflict="user_email,consent_version",
        ).execute()
    except Exception:
        pass
