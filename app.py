import streamlit as st
import pandas as pd
import random
from io import BytesIO

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

        df = df.fillna("")  # 處理 NaN

        # 去除重複留言者
        unique_df = df.drop_duplicates(subset='Name', keep='first')

        if show_comments:
            st.subheader("參加者名單")
            st.dataframe(unique_df[['Name', 'Comment']], use_container_width=True)

        if st.button("🎯 開始抽獎！"):
            st.subheader("🎊 抽獎結果")

            total_participants = unique_df.shape[0]
            if total_participants < 30:
                st.warning("參加者少於 30 位，請確認人數是否足夠。")

            winners = unique_df.sample(n=min(30, total_participants), random_state=42).reset_index(drop=True)

            rice_winners = winners.iloc[:20].reset_index(drop=True)
            rice_winners.insert(0, "編號", range(1, len(rice_winners) + 1))

            bowl_winners = winners.iloc[20:30].reset_index(drop=True)
            bowl_winners.insert(0, "編號", range(1, len(bowl_winners) + 1))

            st.write("🍙 飯糰兌換券 得獎名單（20位）")
            st.dataframe(rice_winners[['編號', 'Name', 'Comment']], use_container_width=True, hide_index=True)

            st.write("🍛 丼飯五折券 得獎名單（10位）")
            st.dataframe(bowl_winners[['編號', 'Name', 'Comment']], use_container_width=True, hide_index=True)

            # 匯出按鈕
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                rice_winners.to_excel(writer, index=False, sheet_name='飯糰兌換券')
                bowl_winners.to_excel(writer, index=False, sheet_name='丼飯五折券')
            output.seek(0)

            st.download_button(
                label="📥 下載得獎名單 Excel",
                data=output,
                file_name="抽獎結果.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"發生錯誤：{e}")
