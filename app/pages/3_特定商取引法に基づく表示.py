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
| 販売価格と送料 | アフターチャットサポート：3,000円/月額 / アフター面談付サポート：19,800円/月額 |
| その他費用 | 特になし |
| 支払い方法 | クレジットカード |
| 支払時期 | 契約締結時より8日以内 |
| 引き渡し時期 | 契約締結時より8日以内 |
| 引き渡し方法 | オンラインでのサポート開始をもって引き渡しとします |
| 役務の提供時期 | 本契約の有効期限は本契約締結日より1ヶ月間とする。前月20日までに申し出がなければ自動更新とする。 |
| 商品代金以外の必要料金 | 消費税 |
| 必要な通信機器、通信回線環境 | インターネット接続10Mbps以上、ZOOM使用、対応OS（Mac/Windows）、複数ブラウザ対応、スマホ受講可 |
| 表現及び商品に関する注意書き | 個人差があり、利益や効果を保証しない |
""")
