import os
import streamlit as st
import pandas as pd
import altair as alt

st.title("총 지각비 꺾은선 그래프")

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

# 총액 열 숫자화 + 학생별 지각비 데이터프레임 구성
df["총액값"] = df["총액"].apply(clean_currency)
plot_df = df.loc[:31, ["이름", "총액값"]].copy()  # 마지막 합계 행 제외

# 이름 기준 정렬 (선택 사항)
plot_df = plot_df.sort_values("이름")

# Altair 꺾은선 그래프
line_chart = (
    alt.Chart(plot_df)
    .mark_line(point=True)
    .encode(
        x=alt.X("이름:N", title="이름"),
        y=alt.Y("총액값:Q", title="총 지각비"),
        tooltip=["이름", alt.Tooltip("총액값:Q", format=",")]
    )
    .properties(width=700, height=400)
)

st.altair_chart(line_chart, use_container_width=True)

