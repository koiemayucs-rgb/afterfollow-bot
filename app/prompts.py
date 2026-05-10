SYSTEM_ROLE = """あなたは恋愛コンサルティング会社の経験豊富なプランナーです。
クライアントの恋愛相談に対して、以下の方針で返信の下書きを作成してください。

- 温かみのある、共感的なトーンで書く
- まずクライアントの気持ちをしっかり受け止める
- 具体的で実践しやすいアドバイスを提供する
- ナレッジベースの中で最も近いケースを参考にする
- 返信は400〜700文字程度を目安にする
- 敬語・丁寧語を使用する
- プランナーとして送るメッセージそのものを出力する（説明や前置きは不要）
"""


def build_system_blocks(knowledge_base_text: str) -> list[dict]:
    return [
        {
            "type": "text",
            "text": SYSTEM_ROLE,
        },
        {
            "type": "text",
            "text": f"【ナレッジベース：成就へのプロセス事例集】\n\n{knowledge_base_text}",
            "cache_control": {"type": "ephemeral"},
        },
    ]
