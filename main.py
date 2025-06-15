import os
import streamlit as st
import pandas as pd
import altair as alt

# 앱 제목
st.title("지각비")

# CSV 파일 경로
csv_path = os.path.join(os.path.dirname(__file__), "data.csv")

# 파일 존재 여부 확인
if not os.path.exists(csv_path):
    st.error(f"파일을 찾을 수 없습니다: {csv_path}")
    st.stop()

# CSV 읽기
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 출석번호 전처리 (.0 제거)
attendance = df["번호"].astype(str).str.replace(r"\.0$", "", regex=True)

# 지각 횟수 (D열: 4번째 열, index 3)
lateness = df.iloc[:, 3].fillna(0).astype(int)

# 시각화용 데이터프레임 생성 및 정렬
plot_df = pd.DataFrame({
    "출석번호": attendance,
    "지각 횟수": lateness
}).sort_values("지각 횟수", ascending=False)

# y축 도메인 고정 (출석번호 전체 표시)
domain_list = plot_df["출석번호"].tolist()

# Altair 가로 막대그래프 생성
chart = (
    alt.Chart(plot_df)
       .mark_bar()
       .encode(
           x=alt.X("지각 횟수:Q", title="지각 횟수", axis=alt.Axis(format="d", tickMinStep=1)),
           y=alt.Y("출석번호:O", title="출석번호", scale=alt.Scale(domain=domain_list),
                   axis=alt.Axis(labelOverlap=False))
       )
       .properties(width=700, height=len(domain_list) * 25)
)

# 그래프 출력
st.altair_chart(chart, use_container_width=True)

# H34 셀 값 추출 및 통화 기호 처리
try:
    raw_value = df.iat[33, 7]  # H34: 34행(인덱스 33), 8번째 열(인덱스 7)
    cleaned_value = str(raw_value).replace("₩", "").replace(",", "").strip()
    total_fee = int(cleaned_value)
    st.markdown(f"### 지각비 총액: {total_fee:,}원")
except Exception as e:
    st.error(f"❌ H34 셀에서 지각비 총액을 불러올 수 없습니다.\n오류: {e}")
