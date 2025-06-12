import os
import streamlit as st

# 이 파일이 실제로 어디에 있는지
st.write("💡 __file__:", os.path.abspath(__file__))

# 스크립트 폴더(이론상 지각비.csv가 있는 곳)
script_dir = os.path.dirname(os.path.abspath(__file__))
st.write("💡 script_dir:", script_dir)

# 그 폴더에 정말 csv가 있는지
csv_path = os.path.join(script_dir, "지각비.csv")
st.write("💡 csv_path:", csv_path)
st.write("💡 exists:", os.path.exists(csv_path))

# 스크립트 폴더 안 파일 목록도 출력
st.write("💡 dir listing:", os.listdir(script_dir))
# streamlit_app.py
import streamlit as st
import pandas as pd
import altair as alt


st.title("지각비 내림차순 가로 막대그래프")

# main/main.py

import os
import pandas as pd
import streamlit as st
import altair as alt

# → 이 부분이 핵심: 스크립트 파일 위치를 기준으로 CSV 경로 생성
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "지각비.csv")

# 이제 이 경로로 읽어 옵니다
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 이하 생략: D열 정렬, 차트 그리기 등…
# 1) CSV 불러오기 (한글 파일이라면 encoding='utf-8-sig' 권장)
df = pd.read_csv("지각비.csv", encoding="utf-8-sig")

# 2) D열 선택 (0-based: 3번 컬럼), 헤더는 첫 번째 행(df.columns)에 이미 빠져 있으므로 바로 사용
#    필요하다면 df.columns 로 컬럼 이름을 확인하세요.
d_series = df.iloc[:, 3]

# 3) 내림차순 정렬
d_sorted = d_series.sort_values(ascending=False)

# 4) 시각화용 DataFrame 생성 (index가 라벨 역할)
plot_df = pd.DataFrame({
    "label": d_sorted.index.astype(str),   # 행 번호 대신 다른 라벨(예: 이름)이 있으면 여기에 넣으세요.
    "value": d_sorted.values
})

# 5) Altair로 가로 막대그래프 생성
chart = (
    alt.Chart(plot_df)
       .mark_bar()
       .encode(
           x=alt.X("value:Q", title="지각비"),
           y=alt.Y(
               "label:O",
               sort=alt.EncodingSortField(
                   field="value",      # value 기준으로
                   op="identity",      # 그 자체 크기(identity)
                   order="descending"  # 내림차순 → 큰 값이 위로
               ),
               title="행 번호"
           )
       )
       .properties(
           width=700,
           height=400
       )
)

# 6) Streamlit에 차트 표시
st.altair_chart(chart, use_container_width=True)
