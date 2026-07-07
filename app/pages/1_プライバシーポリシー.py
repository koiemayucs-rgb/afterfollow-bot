import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st

st.set_page_config(page_title="プライバシーポリシー | Recolor AIサポート", page_icon="🌸")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(160deg, #fff0f4 0%, #fde8f0 100%); }
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 760px !important; padding-top: 2rem !important; }
</style>
""", unsafe_allow_html=True)

st.title("🌸 プライバシーポリシー")
st.caption("最終更新日：2026年7月1日")

st.markdown("""
リカラー株式会社（以下「当社」）は、Recolor AIサポート（以下「本サービス」）における利用者の個人情報の取り扱いについて、以下のとおりプライバシーポリシーを定めます。

---

## 1. 取得する情報

本サービスでは、以下の情報を取得します。

| 情報の種類 | 内容 | 取得方法 |
|---|---|---|
| Googleアカウント情報 | 氏名・メールアドレス（Googleログイン時に取得） | ログイン時に自動取得 |
| 会話内容 | 利用者が入力した恋愛相談のテキスト | サービス利用時に自動取得 |
| 利用状況 | サービスの利用状況（Streamlit のシステムログ） | 自動取得 |

---

## 2. 利用目的

取得した情報は、以下の目的で利用します。

- 本サービス（AI恋愛相談チャット）の提供
- サービスの品質向上・改善
- 障害・不正利用の調査・対応

---

## 3. 第三者への提供

当社は、以下の場合を除き、利用者の個人情報を第三者に提供しません。

- 利用者本人の同意がある場合
- 法令に基づく場合

### 委託先（サブプロセッサ）

本サービスでは、AI 処理のために以下のサービスに会話データを送信します。

| 委託先 | 用途 | 所在地 |
|---|---|---|
| Google LLC | ログイン認証（Google OAuth） | 米国 |
| Anthropic, Inc. | AI（Claude）による返答生成 | 米国 |
| Streamlit, Inc. | アプリホスティング | 米国 |

Anthropic は、商用 API で取得したデータをモデルの学習目的に使用しないポリシーを採用しています。
詳細は [Anthropic のプライバシーポリシー](https://www.anthropic.com/legal/privacy) をご確認ください。

---

## 4. データの保存と管理

| 項目 | 内容 |
|---|---|
| 会話履歴の保存 | **現在はブラウザのセッション内のみ**。ページを閉じると消去されます |
| サーバーへの保存 | 現時点では行っていません |
| 通信の暗号化 | HTTPS により暗号化して通信します |

※ 今後の機能追加によりデータ保存を開始する場合は、本ポリシーを改定のうえ事前にお知らせします。

---

## 5. Cookie・外部サービスの利用

本サービスは Streamlit Community Cloud 上で動作しており、Streamlit が設定する Cookie を使用する場合があります。
Cookie はサービスの動作に必要な範囲で使用し、広告目的では使用しません。

---

## 6. 個人情報に関するお問い合わせ

個人情報の開示・訂正・利用停止等のご請求は、以下の窓口までメールにてご連絡ください。
ご連絡から**30日以内**を目安に対応いたします。

- **事業者名**：リカラー株式会社
- **お問い合わせ先**：info@recolor-inc.net

---

## 7. プライバシーポリシーの改定

当社は、法令の改正やサービス内容の変更に応じて、本ポリシーを改定することがあります。
重要な変更がある場合は、本サービス内でお知らせします。
""")
