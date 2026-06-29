# 🌸 Recolor アフターフォローボット

リカラー卒業生の恋愛相談に寄り添うAIチャットボット。

---

## アプリの概要

| 項目 | 内容 |
|---|---|
| 対象ユーザー | リカラー卒業生（交際中の方） |
| 機能 | 恋愛相談チャット（多ターン会話） |
| AI | Claude Sonnet 4.6（Anthropic） |
| UI | Streamlit（ピンク系チャットデザイン） |
| ホスティング | Streamlit Community Cloud |

### AIの返答スタイル（3ステップ）
1. **感情を受け止める** — 評価せず、まず共感
2. **深掘りする** — 状況を理解するために1つ質問
3. **アドバイスする** — リカラーのナレッジをもとに具体的な提案

### クイック選択ボタン（初回のみ表示）
- 🌙 返信が遅くて不安
- 📅 会う頻度が減った
- 💍 結婚を迷っている
- 😶 気持ちが言えない

---

## ファイル構成

```
afterfollow-bot/
├── app/
│   ├── main.py            # Streamlit UI（チャット画面）
│   ├── claude_client.py   # Claude API 呼び出し
│   ├── prompts.py         # AIのシステムプロンプト（人格・返答ルール）
│   ├── knowledge_base.py  # ナレッジベース読み込み
│   ├── config.py          # 定数・モデル設定
│   └── __init__.py
├── data/
│   ├── recolor_method.txt    # 成就虎の巻（1ヶ月4回デート・PDCA）
│   ├── srank_mindset.txt     # Sランク研修（マインド分析・インナーチャイルド）
│   ├── client_data.csv       # 生徒データ（集計サマリーのみAIに渡す）
│   └── success_process.csv   # 相談事例集
├── main.py                # app/main.py と同内容（Streamlit Cloud用）
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 起動方法

### A. Streamlit Cloud（本番・推奨）

GitHubにpushすると自動でデプロイされます。

1. `git push origin main` でコードを更新
2. Streamlit Cloud（[share.streamlit.io](https://share.streamlit.io)）が自動でデプロイ（2〜3分）
3. URLにアクセスして動作確認

### B. ローカルで動かす（開発・テスト用）

**前提条件**
- Python 3.10 以上
- Anthropic API キー

**手順**

```bash
# 1. リポジトリをクローン
git clone https://github.com/ReColor-dev/afterfollow-bot.git
cd afterfollow-bot

# 2. 依存パッケージをインストール
pip install -r requirements.txt

# 3. APIキーを設定
cp .env.example .env
# .env を開いて ANTHROPIC_API_KEY= の後にキーを貼り付ける

# 4. 起動
streamlit run app/main.py
```

ブラウザが自動で開きます（`http://localhost:8501`）。

---

## 環境変数・シークレット

| 変数名 | 説明 | 設定場所 |
|---|---|---|
| `ANTHROPIC_API_KEY` | AnthropicのAPIキー | ローカル：`.env` / 本番：Streamlit Cloud Secrets |

**Streamlit Cloud でのシークレット設定手順**
1. [share.streamlit.io](https://share.streamlit.io) → アプリを選択
2. `︙` → Settings → Secrets
3. 以下を貼り付けて Save：

```toml
ANTHROPIC_API_KEY = "sk-ant-ここにキーを貼り付ける"
```

---

## ナレッジベースの更新方法

AIが参照する知識は `data/` フォルダのファイルで管理しています。

| ファイル | 更新方法 |
|---|---|
| `recolor_method.txt` | テキストファイルを直接編集してpush |
| `srank_mindset.txt` | テキストファイルを直接編集してpush |
| `success_process.csv` | CSVを編集してpush |
| `client_data.csv` | 新しいデータに差し替えてpush |

pushすると自動で反映されます。

---

## AIの人格・返答を変えたい場合

`app/prompts.py` の `BOT_SYSTEM_ROLE` を編集します。

- 口調・トーンを変える → `## 話し方のルール` を編集
- 返答の型を変える → `## 返答の3ステップ` を編集
- 対応する悩みを追加する → `## 対応する悩みの例` を追加

編集後 `git push` で反映されます。

---

## 使用技術・サービス

| サービス | 用途 | 費用 |
|---|---|---|
| [Anthropic API](https://console.anthropic.com) | AI（Claude Sonnet 4.6） | 従量課金（1会話 約$0.005〜$0.01） |
| [Streamlit Community Cloud](https://share.streamlit.io) | ホスティング | 無料 |
| [GitHub](https://github.com/ReColor-dev/afterfollow-bot) | コード管理・自動デプロイ | 無料 |

---

## 今後の実装予定

- [ ] Googleアカウントでのログイン機能
- [ ] ユーザーごとの会話履歴の保存
- [ ] 管理画面（会話ログの確認）
