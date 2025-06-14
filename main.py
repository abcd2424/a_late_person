import os
import streamlit as st
import pandas as pd
import altair as alt

# — 디버깅: 실제 파일 위치와 존재 여부 확인 —
st.write("💡 __file__:", os.path.abspath(__file__))
script_dir = os.path.dirname(os.path.abspath(__file__))
st.write("💡 script_dir:", script_dir)
csv_path = os.path.join(script_dir, "data.csv")
st.write("💡 csv_path:", csv_path)
st.write("💡 exists:", os.path.exists(csv_path))
st.write("💡 dir listing:", os.listdir(script_dir))

# — 앱 제목 —
st.title("지각비 내림차순 가로 막대그래프")

# — CSV 읽기 —
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
else:
    st.error(f"파일을 찾을 수 없습니다: {csv_path}")
    st.stop()

# — 1) 출석번호(첫 번째 열), 2) 지각 횟수(D열) 가져오기 —
attendance = df.iloc[1:, 0].astype(str)                  # A열에 출석번호가 있다고 가정
lateness = df.iloc[1:, 3].fillna(0).astype(int)          # D열의 빈값은 0으로 채움

# — 시각화용 DataFrame 생성 및 내림차순 정렬 —
plot_df = pd.DataFrame({
    "출석번호": attendance,
    "지각 횟수": lateness
})
plot_df = plot_df.sort_values("지각 횟수", ascending=False)

# — 가로 막대그래프 생성 —
chart = (
    alt.Chart(plot_df)
       .mark_bar()
       .encode(
           x=alt.X(
               "지각 횟수:Q",
               title="지각 횟수",
               axis=alt.Axis(format='d', tickMinStep=1)
           ),
           y=alt.Y(
               "출석번호:O",
               sort=alt.EncodingSortField("지각 횟수", order="descending"),
               title="출석번호"
           )
       )
       .properties(width=700, height=400)
)

# — 차트 표시 —
st.altair_chart(chart, use_container_width=True)
