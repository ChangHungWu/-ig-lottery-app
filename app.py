import streamlit as st
import pandas as pd
import random

st.title("🎁 IG留言抽獎系統")

uploaded_file = st.file_uploader("📂 請上傳留言 Excel 檔案", type=["xlsx"])
show_comments = st.checkbox("✅ 顯示參加者留言內容")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # 檢查必要欄位
        if 'Name' not in df.columns or 'Comment' not in df.columns:
            st.error("❌ Excel 檔案必須包含『Name』與『Comment』欄")
            st.stop()

        # 處理缺失值，避免 NaN 造成錯誤
        df = df.fillna("")

        # 移除重複的參加者（根據 Name）
        unique_df = df.drop_duplicates(subset='Name', keep='first')

        if show_comments:
            st.subheader("參加者名單")
            st.dataframe(unique_df[['Name', 'Comment']])

        if st.button("🎯 開始抽獎！"):
            st.subheader("🎊 抽獎結果")

            total_participants = unique_df.shape[0]
            if total_participants < 30:
                st.warning("參加者少於 30 位，請確認人數是否足夠。")

            winners = unique_df.sample(n=min(30, total_participants), random_state=42).reset_index(drop=True)

            rice_winners = winners.iloc[:20]
            bowl_winners = winners.iloc[20:30]

            st.write("🍙 飯糰兌換券 得獎名單（20位）")
            st.table(rice_winners[['Name', 'Comment']])

            st.write("🍛 丼飯五折券 得獎名單（10位）")
            st.table(bowl_winners[['Name', 'Comment']])

    except Exception as e:
        st.error(f"發生錯誤：{e}")
