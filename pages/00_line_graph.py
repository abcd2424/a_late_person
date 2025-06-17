import os
import streamlit as st
import pandas as pd
import altair as alt

st.title("지각 횟수 원 그래프 (상위 10명 + 기타)")

# 데이터 불러오기
csv_path = os.path.join(os.path.dirname(__file__), "../data.csv")
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 지각 횟수 정제
df["지각 횟수"] = df.iloc[:, 3].fillna(0).astype(int)

# 상위 10명 + 기타
top10 = df.nlargest(10, "지각 횟수")[["이름", "지각 횟수"]]
others = df[~df["이름"].isin(top10["이름"])]
others_sum = pd.DataFrame([{"이름": "기타", "지각 횟수": int(others["지각 횟수"].sum())}])
final_df = pd.concat([top10, others_sum], ignore_index=True)
final_df = final_df.sort_values("지각 횟수", ascending=False).reset_index(drop=True)

# Vega-Lite 베이스
base = alt.Chart(final_df).encode(
    theta=alt.Theta("지각 횟수:Q", stack=True),
    color=alt.Color("이름:N", scale=alt.Scale(scheme="category20b"), title="이름"),
    order=alt.Order("지각 횟수:Q", sort="descending")
)

# 파이 조각
pie = base.mark_arc(innerRadius=0, outerRadius=180).encode(
    tooltip=[alt.Tooltip("이름:N"), alt.Tooltip("지각 횟수:Q")]
)

# 중앙 라벨
labels = base.mark_text(radius=110, size=13, fontWeight="bold").encode(
    text=alt.Text("이름:N"),
    color=alt.value("white")
)

# 레이어 결합 + 높이 지정
chart = alt.layer(pie, labels).properties(
    width=400,    # 필요에 따라 조절
    height=400    # outerRadius*2 이상으로 설정
)

st.altair_chart(chart, use_container_width=True)
