import os
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.title("총 지각비 원 그래프 (상위 10명 + 기타)")

# CSV 경로
csv_path = os.path.join(os.path.dirname(__file__), "../data.csv")

# 데이터 불러오기
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 통화 → 정수로 변환
def clean_currency(val):
    try:
        return int(str(val).replace("₩", "").replace(",", "").strip())
    except:
        return 0

# 총액 숫자화
df["총액값"] = df["총액"].apply(clean_currency)
plot_df = df.loc[:31, ["이름", "총액값"]].copy()
plot_df = plot_df[plot_df["총액값"] > 0]

# 상위 10명 + 기타
top10 = plot_df.nlargest(10, "총액값")
others = plot_df[~plot_df["이름"].isin(top10["이름"])]
others_sum = pd.DataFrame([{"이름": "기타", "총액값": others["총액값"].sum()}])
final_df = pd.concat([top10, others_sum], ignore_index=True)

# 퍼센트 및 좌표 계산
final_df["비율"] = final_df["총액값"] / final_df["총액값"].sum()
final_df["누적"] = final_df["비율"].cumsum()
final_df["시작"] = final_df["누적"] - final_df["비율"]
final_df["각도"] = (final_df["시작"] + final_df["비율"] / 2) * 2 * np.pi

# ✅ 라벨 위치 조정 (더 안쪽으로)
label_radius = 85
final_df["x"] = final_df["각도"].apply(lambda a: label_radius * np.cos(a))
final_df["y"] = final_df["각도"].apply(lambda a: label_radius * np.sin(a))

# 파이 차트
pie = (
    alt.Chart(final_df)
    .mark_arc()
    .encode(
        theta=alt.Theta("총액값:Q"),
        color=alt.Color("이름:N", scale=alt.Scale(scheme='category20'), title="이름"),
        tooltip=["이름:N", alt.Tooltip("총액값:Q", format=",")]
    )
    .properties(width=500, height=500)
)

# 텍스트 라벨
labels = (
    alt.Chart(final_df)
    .mark_text(size=13, fontWeight="bold")  # 글자 크기/굵기 조절
    .encode(
        x=alt.X("x:Q", axis=None),
        y=alt.Y("y:Q", axis=None),
        text=alt.Text("이름:N"),
        color=alt.value("white")  # 어두운 배경에서도 잘 보이게 흰색 고정
    )
)

# 최종 출력
st.altair_chart(pie + labels, use_container_width=True)
