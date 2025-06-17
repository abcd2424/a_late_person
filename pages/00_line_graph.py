import os
import streamlit as st
import pandas as pd
import altair as alt

st.title("총 지각비 원 그래프")

# CSV 경로
csv_path = os.path.join(os.path.dirname(__file__), "../data.csv")

# 데이터 불러오기
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 통화 → 정수로 변환 함수
def clean_currency(val):
    try:
        return int(str(val).replace("₩", "").replace(",", "").strip())
    except:
        return 0

# 총액 숫자화 + 마지막 행(합계) 제외
df["총액값"] = df["총액"].apply(clean_currency)
plot_df = df.loc[:31, ["이름", "총액값"]].copy()

# 총액이 0 이상인 사람만 필터링 (지각 안 한 사람 제외)
plot_df = plot_df[plot_df["총액값"] > 0]

# 파이 차트 생성
pie = (
    alt.Chart(plot_df)
    .mark_arc()
    .encode(
        theta=alt.Theta("총액값:Q", title="총액 비율"),
        color=alt.Color("이름:N", legend=None),
        tooltip=["이름", alt.Tooltip("총액값:Q", format=",")]
    )
    .properties(width=500, height=500)
)

st.altair_chart(pie, use_container_width=True)
