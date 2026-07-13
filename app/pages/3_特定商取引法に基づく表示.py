import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st

st.set_page_config(page_title="特定商取引法に基づく表示 | ReColor AIサポート", page_icon="🌸")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(160deg, #fff0f4 0%, #fde8f0 100%); }
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 760px !important; padding-top: 2rem !important; }
</style>
""", unsafe_allow_html=True)

st.title("📋 特定商取引法に基づく表示")

st.markdown("""
| 項目 | 内容 |
|---|---|
| 販売業者 | 株式会社リカラー |
| 業務責任者 | 大塚 都 |
| 住所 | 〒150-0036 東京都渋谷区南平台町16-28 Daiwa渋谷スクエア 6階 |
| 法人番号 | 6010001237691 |
| 電話番号 | 03-6824-1535 |
| メールアドレス | info@recolor-inc.net |
| 販売価格と送料 | 無料カウンセリング：0円 / トライアルコース：330,000円(税込) / ライトコース：660,000円(税込) / スタンダードコース：1,100,000円(税込) / シンデレラコース：1,430,000円(税込) / 各コース入会金一律55,000円(税込) |
| その他費用 | 特になし |
| 支払い方法 | クレジットカード、銀行振込、ショッピングクレジット |
| 支払時期 | 契約締結時より8日以内 |
| 引き渡し時期 | 契約締結時より8日以内 |
| 引き渡し方法 | オンラインでのサポート開始をもって引き渡しとします |
| 役務の提供時期 | トライアルコース：契約締結日より60日間 / ライトコース：契約締結日より180日間 / スタンダードコース：契約締結日より210日間 / シンデレラコース：契約締結日より330日間 |
| 商品代金以外の必要料金 | 消費税、決済手数料（銀行振込み時手数料） |
| 返品・交換・キャンセル等 | 契約締結時より8日間はクーリングオフが可能 |
| 必要な通信機器、通信回線環境 | インターネット接続10Mbps以上、ZOOM使用、対応OS（Mac/Windows）、複数ブラウザ対応、スマホ受講可 |
| 表現及び商品に関する注意書き | 個人差があり、利益や効果を保証しない |
""")
