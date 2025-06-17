import os
import streamlit as st
import pandas as pd
import altair as alt

st.title("총 지각비 원 그래프 (상위 10명 + 기타)")

import numpy as np

# CSV 경로
csv_path = os.path.join(os.path.dirname(__file__), "../data.csv")
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 통화 → 정수 변환
def clean_currency(val):
    try:
        return int(str(val).replace("₩", "").replace(",", "").strip())
    except:
        return 0

df["총액값"] = df["총액"].apply(clean_currency)
plot_df = df.loc[:31, ["이름", "총액값"]].copy()
plot_df = plot_df[plot_df["총액값"] > 0]

# 상위 10명 + 기타
top10 = plot_df.nlargest(10, "총액값")
others = plot_df[~plot_df["이름"].isin(top10["이름"])]
others_sum = pd.DataFrame([{"이름": "기타", "총액값": others["총액값"].sum()}])
final_df = pd.concat([top10, others_sum], ignore_index=True)

# 파이 차트
base = alt.Chart(final_df).encode(
    theta=alt.Theta("총액값:Q", stack=True),
    color=alt.Color("이름:N", scale=alt.Scale(scheme='category20b'), title="이름")
)

# 원 그래프
pie = base.mark_arc(innerRadius=0, outerRadius=180).encode(
    tooltip=["이름:N", alt.Tooltip("총액값:Q", format=",")]
)

# ✅ 정확한 중심 각도에 이름 표시
labels = base.mark_text(radius=110, size=13, fontWeight="bold").encode(
    text="이름:N",
    color=alt.value("white")
)

# 출력
st.altair_chart(pie + labels, use_container_width=True)
