import os
import streamlit as st
import pandas as pd
import altair as alt

# — 앱 제목 —
st.title("지각비 내림차순 가로 막대그래프")

# — CSV 경로 설정 및 읽기 —
csv_path = os.path.join(os.path.dirname(__file__), "data.csv")
if not os.path.exists(csv_path):
    st.error(f"파일을 찾을 수 없습니다: {csv_path}")
    st.stop()
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# — 출석번호(번호)와 지각 횟수 컬럼 추출 —
attendance = df["번호"].fillna(0).astype(int).astype(str)    # “.0” 제거
lateness   = df.iloc[:, 3].fillna(0).astype(int)            # D열(4번째) 지각 횟수, 빈값은 0

# — 시각화용 DataFrame 생성 및 내림차순 정렬 —
plot_df = pd.DataFrame({
    "출석번호": attendance,
    "지각 횟수": lateness
}).sort_values("지각 횟수", ascending=False)

# — 가로 막대그래프 생성 —
chart = (
    alt.Chart(plot_df)
       .mark_bar()
       .encode(
           y=alt.Y(
               "출석번호:O",
               sort=alt.EncodingSortField("지각 횟수", order="descending"),
               title="출석번호",
               axis=alt.Axis(labelOverlap=False)   # 모든 라벨 표시
           ),
           x=alt.X(
               "지각 횟수:Q",
               title="지각 횟수",
               axis=alt.Axis(format="d", tickMinStep=1)  # 정수 눈금
           )
       )
       .properties(width=700, height=400)
)

# — 차트 표시 —
st.altair_chart(chart, use_container_width=True)
