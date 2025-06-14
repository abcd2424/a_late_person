import os
import streamlit as st
import pandas as pd
import altair as alt

# 디버깅: 실제 파일 위치와 존재 여부 확인
st.write("💡 __file__:", os.path.abspath(__file__))
script_dir = os.path.dirname(os.path.abspath(__file__))
st.write("💡 script_dir:", script_dir)
csv_path = os.path.join(script_dir, "data.csv")
st.write("💡 csv_path:", csv_path)
st.write("💡 exists:", os.path.exists(csv_path))
st.write("💡 dir listing:", os.listdir(script_dir))

# 앱 제목
st.title("지각비 내림차순 가로 막대그래프")

# CSV 읽기
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
else:
    st.error(f"파일을 찾을 수 없습니다: {csv_path}")
    st.stop()

# D열 선택 (0-based 인덱스 3 -> D열), 두 번째 행부터 (헤더 제외)
d_series = df.iloc[1:, 3].astype(float)

# 내림차순 정렬
d_sorted = d_series.sort_values(ascending=False)

# 시각화용 DataFrame 생성
plot_df = pd.DataFrame({
    "label": d_sorted.index.astype(str),
    "value": d_sorted.values
})

# 가로 막대그래프 생성
chart = (
    alt.Chart(plot_df)
       .mark_bar()
       .encode(
           x=alt.X(
               "value:Q",
               title="지각비",
               axis=alt.Axis(
                   format='d',        # 정수 포맷 (소수점 제거)
                   tickMinStep=1      # 눈금 최소 간격을 1로 설정
               )
           ),
           y=alt.Y(
               "label:O",
               sort=alt.EncodingSortField(field="value", order="descending"),
               title="행 번호"
           )
       )
       .properties(width=700, height=400)
)

# 차트 표시
st.altair_chart(chart, use_container_width=True)
