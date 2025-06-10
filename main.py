pip install streamlit pandas altair openpyxl
import streamlit as st
import pandas as pd
import altair as alt

st.title("지각비 내림차순 가로 막대그래프")

# 1) Excel 파일 로드
#    - header=0 으로 첫 행(D1)을 컬럼명으로 사용
df = pd.read_excel("지각비.xltx", header=0, engine="openpyxl")

# 2) D열 이름 추출 (0-based 인덱스 3이 D열)
d_col = df.columns[3]

# 3) 내림차순 정렬
df_sorted = df.sort_values(by=d_col, ascending=False).reset_index(drop=True)

# 4) 레이블로 사용할 컬럼 지정 (여기서는 첫 번째 컬럼이라고 가정)
label_col = df_sorted.columns[0]

# 5) Altair로 가로 막대그래프 생성
chart = (
    alt.Chart(df_sorted)
    .mark_bar()
    .encode(
        x=alt.X(f"{d_col}:Q", title=d_col),
        y=alt.Y(f"{label_col}:N", sort='-x', title=label_col)  # '-x'로 높은 값이 위로
    )
    .properties(width=700, height=400)
)

# 6) Streamlit에 차트 표시
st.altair_chart(chart, use_container_width=True)
streamlit run app.py
