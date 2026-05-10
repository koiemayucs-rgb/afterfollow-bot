# Slack ボット移行ガイド

プロトタイプ（Streamlit Web アプリ）を Slack ボットに移行する手順です。
`app/claude_client.py` の `draft_reply()` はそのまま再利用できます。

## 追加インストール

```bash
pip install slack-bolt
```

## Slack App の設定

1. https://api.slack.com/apps でアプリを新規作成
2. **OAuth & Permissions** → Bot Token Scopes に `chat:write` を追加
3. **Event Subscriptions** → `app_mention` イベントを有効化
4. **Socket Mode** を有効化（開発初期はこちらが簡単）
5. Bot Token (`xoxb-...`) と App-Level Token (`xapp-...`) を `.env` に追加

```
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
```

## ハンドラコード（slack_bot/handler.py）

```python
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from app.claude_client import draft_reply  # ← そのまま使う

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("app_mention")
def handle_mention(event, say):
    # @ボット名 の部分を除いた本文を相談テキストとして使う
    text = " ".join(event["text"].split()[1:]).strip()
    if not text:
        say(text="相談内容を @メンション の後に入力してください。", thread_ts=event["ts"])
        return

    say(text="生成中...", thread_ts=event["ts"])
    draft, _ = draft_reply(text)

    say(
        text=f"📝 *返信ドラフト*\n\n{draft}\n\n_（必ず確認・編集してから送信してください）_",
        thread_ts=event["ts"],
    )

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
```

## 起動

```bash
python slack_bot/handler.py
```

## 使い方

プランナーが Slack で対象チャンネルに以下のように入力する：

```
@ボット名 クライアントの相談文をここにペースト...
```

→ ボットがスレッドに返信ドラフトを投稿する。
