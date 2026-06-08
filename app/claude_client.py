import anthropic
from app.config import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS
from app.knowledge_base import load_knowledge_base
from app.prompts import build_system_blocks, build_chat_system_blocks

_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def chat_reply(messages: list[dict]) -> tuple[str, dict]:
    """
    会話履歴を受け取り、次のAI返答を生成する（チャットボット用）。

    Args:
        messages: [{"role": "user"|"assistant", "content": "..."}, ...] の会話履歴

    Returns:
        (reply_text, usage_stats)
    """
    kb_text = load_knowledge_base()
    system_blocks = build_chat_system_blocks(kb_text)

    response = _client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system_blocks,
        messages=messages,
    )

    reply = next(
        (block.text for block in response.content if block.type == "text"), ""
    )

    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cache_creation_tokens": getattr(response.usage, "cache_creation_input_tokens", 0) or 0,
        "cache_read_tokens": getattr(response.usage, "cache_read_input_tokens", 0) or 0,
    }

    return reply, usage


def draft_reply(consultation_text: str) -> tuple[str, dict]:
    """
    恋愛相談テキストに対する返信ドラフトを生成する（旧プランナーツール用）。
    """
    kb_text = load_knowledge_base()
    system_blocks = build_system_blocks(kb_text)

    response = _client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system_blocks,
        messages=[
            {
                "role": "user",
                "content": (
                    "以下のクライアントからの相談メッセージに対する返信の下書きを作成してください。\n\n"
                    f"【相談内容】\n{consultation_text}"
                ),
            }
        ],
    )

    draft = next(
        (block.text for block in response.content if block.type == "text"), ""
    )

    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cache_creation_tokens": getattr(response.usage, "cache_creation_input_tokens", 0) or 0,
        "cache_read_tokens": getattr(response.usage, "cache_read_input_tokens", 0) or 0,
    }

    return draft, usage
