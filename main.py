import os
import streamlit as st
import pandas as pd
import altair as alt

# 앱 제목
st.title("지각비")

# CSV 경로
csv_path = os.path.join(os.path.dirname(__file__), "data.csv")

# 파일 불러오기
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 출석번호 처리 (.0 제거)
attendance = df["번호"].astype(str).str.replace(r"\.0$", "", regex=True)

# 지각 횟수 처리 (D열)
lateness = df.iloc[:, 3].fillna(0).astype(int)

# 미납금(G열) 정제 함수
def clean_currency(val):
    try:
        return int(str(val).replace("₩", "").replace(",", "").strip())
    except:
        return 0

# 시각화용 데이터 정리
plot_df = pd.DataFrame({
    "출석번호": attendance,
    "이름": df["이름"],
    "지각 횟수": lateness,
    "총액": df["총액"],
    "미납금값": df["남은금액"].apply(clean_currency)
}).iloc[:32]  # 마지막 합계행 제외

# 지각 횟수 0 이상만 필터링
plot_df = plot_df[plot_df["지각 횟수"] > 0]

# 미납금 텍스트
plot_df["미납금"] = plot_df["미납금값"].apply(lambda x: f"미납금: ₩{x:,}")

# 정렬
plot_df = plot_df.sort_values("지각 횟수", ascending=False)
domain_list = plot_df["이름"].tolist()  # 이름 기준 정렬

# Altair 그래프
chart = (
    alt.Chart(plot_df)
       .mark_bar()
       .encode(
           x=alt.X("지각 횟수:Q", title="지각 횟수", axis=alt.Axis(format="d", tickMinStep=1)),
           y=alt.Y("이름:O", scale=alt.Scale(domain=domain_list),
                   axis=alt.Axis(labelOverlap=False, title=None)),  # 👉 y축 라벨 제거
           tooltip=[
               alt.Tooltip("이름"),
               alt.Tooltip("미납금", title="")
           ]
       )
       .properties(width=700, height=len(domain_list) * 25)
)

# 그래프 출력
st.altair_chart(chart, use_container_width=True)

# 지각비 총액 출력 (엑셀 H34 = 33번째 행, '남은금액' 열)
try:
    raw_value = df.at[32, "남은금액"]
    cleaned_value = str(raw_value).replace("₩", "").replace(",", "").strip()
    total_fee = int(cleaned_value)
    st.markdown(f"### 지각비 총액: {total_fee:,}원")
except Exception as e:
    st.error(f"❌ 지각비 총액을 불러올 수 없습니다.\n오류: {e}")
