import os
import streamlit as st
import pandas as pd
import altair as alt

st.title("총 지각비 원 그래프 (상위 10명 + 기타)")

# CSV 경로
csv_path = os.path.join(os.path.dirname(__file__), "../data.csv")

# 데이터 불러오기
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 통화 → 정수로 변환 함수
def clean_currency(val):
    try:
        return int(str(val).replace("₩", "").replace(",", "").strip())
    except:
        return 0

# 총액 숫자화
df["총액값"] = df["총액"].apply(clean_currency)
plot_df = df.loc[:31, ["이름", "총액값"]].copy()  # 마지막 합계행 제외
plot_df = plot_df[plot_df["총액값"] > 0]  # 총액 0 이상 필터링

# 상위 10명 추출
top10 = plot_df.nlargest(10, "총액값")
others = plot_df[~plot_df["이름"].isin(top10["이름"])]

# "기타" 그룹 생성
others_sum = pd.DataFrame([{
    "이름": "기타",
    "총액값": others["총액값"].sum()
}])

# 상위 10명 + 기타 합치기
final_df = pd.concat([top10, others_sum], ignore_index=True)

# 총합 계산 → 퍼센트 표시용
total = final_df["총액값"].sum()
final_df["비율"] = final_df["총액값"] / total

# 파이 차트
pie = (
    alt.Chart(final_df)
    .mark_arc()
    .encode(
        theta=alt.Theta("총액값:Q", title=""),
        color=alt.Color("이름:N", title="이름"),
        tooltip=["이름", alt.Tooltip("총액값:Q", format=",")]
    )
    .properties(width=500, height=500)
)

# 텍스트 레이블 (이름)
labels = (
    alt.Chart(final_df)
    .mark_text(radius=170, size=13)
    .encode(
        theta=alt.Theta("총액값:Q"),
        text=alt.Text("이름:N"),
        color=alt.value("black")  # 텍스트 색상
    )
)

# 차트 + 레이블 결합
chart = pie + labels

# 출력
st.altair_chart(chart, use_container_width=True)
