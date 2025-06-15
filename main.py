import os
import streamlit as st
import pandas as pd
import altair as alt

# 앱 제목
st.title("지각비")

# CSV 읽기
csv_path = os.path.join(os.path.dirname(__file__), "data.csv")
if not os.path.exists(csv_path):
    st.error(f"파일을 찾을 수 없습니다: {csv_path}")
    st.stop()

df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 1) 출석번호: .0 제거
attendance = (
    df["번호"]
      .astype(str)
      .str.replace(r"\.0$", "", regex=True)
)

# 2) 지각 횟수(D열): 빈값→0, 정수형
lateness = df.iloc[:, 3].fillna(0).astype(int)

# DataFrame 생성 및 내림차순 정렬
plot_df = pd.DataFrame({
    "출석번호": attendance,
    "지각 횟수": lateness
})
plot_df = plot_df.sort_values("지각 횟수", ascending=False)

# y축 도메인 리스트 (출석번호 순서대로)
domain_list = plot_df["출석번호"].tolist()

# 차트
chart = (
    alt.Chart(plot_df)
       .mark_bar()
       .encode(
           x=alt.X(
               "지각 횟수:Q",
               title="지각 횟수",
               axis=alt.Axis(format="d", tickMinStep=1)
           ),
           y=alt.Y(
               "출석번호:O",
               title="출석번호",
               scale=alt.Scale(domain=domain_list),      # 모든 카테고리 강제 표시
               axis=alt.Axis(labelOverlap=False)         # 라벨 간섭 방지
           )
       )
       .properties(
           width=700,
           height=len(domain_list) * 25               # 행 수만큼 세로 크기 확보
       )
)

st.altair_chart(chart, use_container_width=True)
