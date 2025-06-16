import os
import streamlit as st
import pandas as pd
import altair as alt

# 앱 제목
st.title("지각비")

# CSV 경로
csv_path = os.path.join(os.path.dirname(__file__), "data.csv")

# CSV 파일 불러오기
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 출석번호 처리 (.0 제거)
attendance = df["번호"].astype(str).str.replace(r"\.0$", "", regex=True)

# 지각 횟수 처리 (D열)
lateness = df.iloc[:, 3].fillna(0).astype(int)

# 통화 정제 함수
def clean_currency(val):
    try:
        return int(str(val).replace("₩", "").replace(",", "").strip())
    except:
        return 0

# 시각화용 데이터프레임 생성
plot_df = pd.DataFrame({
    "출석번호": attendance,
    "이름": df["이름"],
    "지각 횟수": lateness,
    "총액값": df["총액"].apply(clean_currency),
    "미납금값": df["남은금액"].apply(clean_currency)
}).iloc[:32]  # 합계 행 제외

# 지각 횟수 0 이상만 필터링
plot_df = plot_df[plot_df["지각 횟수"] > 0]

# 낸 금액 계산
plot_df["낸금액값"] = plot_df["총액값"] - plot_df["미납금값"]

# 표시용 텍스트 생성
plot_df["총액"] = plot_df["총액값"].apply(lambda x: f": ₩{x:,}")
plot_df["미납금"] = plot_df["미납금값"].apply(lambda x: f": ₩{x:,}")

# 이름 기준 정렬
plot_df = plot_df.sort_values("지각 횟수", ascending=False)
domain_list = plot_df["이름"].tolist()

# 데이터 분할 (스택 그래프용)
melt_df = pd.melt(
    plot_df,
    id_vars=["이름"],
    value_vars=["낸금액값", "미납금값"],
    var_name="구분",
    value_name="금액"
)

# 보기 좋게 이름 매핑
melt_df["구분"] = melt_df["구분"].map({
    "낸금액값": "납부 완료",
    "미납금값": "미납"
})

# 이름 순서 고정
melt_df["이름"] = pd.Categorical(melt_df["이름"], categories=domain_list, ordered=True)

# Altair 스택 그래프
chart = (
    alt.Chart(melt_df)
    .mark_bar()
    .encode(
        x=alt.X("금액:Q", title="금액 (₩)", axis=alt.Axis(format="d", tickMinStep=1000)),
        y=alt.Y("이름:O", sort=domain_list, title=None),
        color=alt.Color("구분:N", scale=alt.Scale(scheme="tableau10")),
        tooltip=[
            alt.Tooltip("이름:N"),
            alt.Tooltip("구분:N"),
            alt.Tooltip("금액:Q", format=",.0f", title="금액 (₩)")
        ]
    )
    .properties(width=700, height=len(domain_list) * 25)
)

# 그래프 출력
st.altair_chart(chart, use_container_width=True)

# 지각비 총액 출력 (엑셀 H34 = index 32, '남은금액' 열)
try:
    raw_total = df.at[32, "남은금액"]
    cleaned_total = str(raw_total).replace("₩", "").replace(",", "").strip()
    total_fee = int(cleaned_total)
    st.markdown(f"### 지각비 총액: {total_fee:,}원")
except Exception as e:
    st.error(f"❌ 지각비 총액을 불러올 수 없습니다.\n오류: {e}")

# 미납금 총합 출력 (남은금액 열의 마지막 행)
try:
    raw_balance = df["남은금액"].iloc[-1]
    cleaned_balance = str(raw_balance).replace("₩", "").replace(",", "").strip()
    total_balance = int(cleaned_balance)
    st.markdown(f"### 미납금 총액: {total_balance:,}원")
except Exception as e:
    st.error(f"❌ 미납금 총액을 불러올 수 없습니다.\n오류: {e}")
