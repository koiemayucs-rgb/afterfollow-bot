import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st

st.set_page_config(page_title="外国にある事業者への情報の提供について | ReColor AIサポート", page_icon="🌸")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(160deg, #fff0f4 0%, #fde8f0 100%); }
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 760px !important; padding-top: 2rem !important; }
</style>
""", unsafe_allow_html=True)

st.title("🌸 外国にある事業者への情報の提供について")
st.caption("バージョン 1.0　／　2026年7月13日")

st.markdown("""
株式会社リカラー（以下「当社」）は、ReColor AIサポートの提供にあたり、個人情報保護法第28条に基づき、外国にある事業者（以下「外国事業者」）への個人情報の提供に関して、以下のとおり情報を提供します。

---

## 第1条　提供先の外国

本サービスでは、以下の国にある事業者に個人情報を提供します。

| 国名 | 備考 |
|---|---|
| **米国（アメリカ合衆国）** | 一部データは日本国内（東京リージョン）のサーバーに保存されますが、事業者自体は米国に所在します（Supabase, Inc. 参照） |

---

## 第2条　米国における個人情報の保護に関する制度

米国には、日本の個人情報保護法に相当する**包括的な連邦個人情報保護法は存在しません**。
主な制度上の特徴は以下のとおりです。

| 項目 | 内容 |
|---|---|
| 包括的連邦法 | 現時点では存在しない（州ごとの個別法は存在） |
| 独立した監督機関 | 日本の個人情報保護委員会に相当する統一的な監督機関は存在しない |
| 捜査機関へのアクセス | CLOUD Act・FISA（外国情報監視法）等に基づき、米国当局が一定の条件下でデータにアクセスできる場合がある |
| 州法 | カリフォルニア州（CCPA/CPRA）等、一部の州では強力な保護規定を設けている |

---

## 第3条　外国事業者の概要および安全管理措置

| 項目 | Anthropic, Inc. | Supabase, Inc. |
|---|---|---|
| 所在地 | 米国カリフォルニア州サンフランシスコ | 米国カリフォルニア州サンフランシスコ |
| 利用目的 | AIによる返答の生成 | 会話履歴データベースの管理 |
| 提供する情報 | 会話テキスト | メールアドレス・会話テキスト |
| データ保存先 | 米国 | **東京リージョン（日本国内）** |
| 学習利用 | 商用APIで取得したデータはモデル学習に使用しない（Anthropicポリシー準拠） | 対象外 |
| 安全管理措置 | TLS暗号化・アクセス制御・SOC 2準拠 | TLS暗号化・アクセス制御・SOC 2 Type 2準拠 |
| プライバシーポリシー | [anthropic.com/legal/privacy](https://www.anthropic.com/legal/privacy) | [supabase.com/privacy](https://supabase.com/privacy) |

---

## 第4条　同意の任意性と非同意の場合の影響

1. 外国事業者への情報提供についての同意は、任意です。
2. ただし、**同意いただけない場合は、本サービスをご利用いただくことができません**。本サービスはAnthropicおよびSupabaseを利用して構築されており、これらへの情報提供なしにサービスを提供することができないためです。
3. 同意を撤回する場合は、下記お問い合わせ窓口へご連絡ください。撤回後はサービスの利用を停止し、保存済みデータの削除手続きを行います。

---

## 第5条　お問い合わせ

本書に関するお問い合わせは、以下の窓口までご連絡ください。

- **事業者名**：株式会社リカラー
- **住所**：〒150-0036 東京都渋谷区南平台町16-28 Daiwa渋谷スクエア 6階
- **メールアドレス**：info@recolor-inc.net
""")
