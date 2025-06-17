import os
import streamlit as st
import pandas as pd
import altair as alt

st.title("지각 횟수 원 그래프 (상위 10명 + 기타)")

# CSV 경로
csv_path = os.path.join(os.path.dirname(__file__), "../data.csv")

# 데이터 불러오기
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 지각 횟수 컬럼 정제 (D열 가정)
df["지각 횟수"] = df.iloc[:, 3].fillna(0).astype(int)

# 상위 10명 추출
top10 = df.nlargest(10, "지각 횟수")[["이름", "지각 횟수"]].copy()

# 기타 그룹 생성
others = df[~df["이름"].isin(top10["이름"])]
others_sum = pd.DataFrame([{
    "이름": "기타",
    "지각 횟수": int(others["지각 횟수"].sum())
}])

# 최종 데이터프레임 결합 및 내림차순 정렬
final_df = pd.concat([top10, others_sum], ignore_index=True)
final_df = final_df.sort_values("지각 횟수", ascending=False).reset_index(drop=True)

# Vega-Lite 차트 베이스
base = alt.Chart(final_df).encode(
    theta=alt.Theta("지각 횟수:Q", stack=True),               # 파이 각도 기준
    color=alt.Color(                                         
        "이름:N",
        sort=final_df["이름"].tolist(),                     # 범례 및 그리기 순서 고정
        scale=alt.Scale(scheme="category20b"),
        title="이름"
    )
)

# 파이 차트
pie = base.mark_arc(innerRadius=0, outerRadius=180).encode(
    tooltip=[
        alt.Tooltip("이름:N", title="이름"),
        alt.Tooltip("지각 횟수:Q", title="지각 횟수")
    ]
)

# 조각 중앙에 이름 라벨
labels = base.mark_text(radius=110, size=13, fontWeight="bold").encode(
    text=alt.Text("이름:N"),
    color=alt.value("white")
)

# 차트 출력
st.altair_chart(pie + labels, use_container_width=True)
