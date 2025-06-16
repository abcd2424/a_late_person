import os
import streamlit as st
import pandas as pd
import altair as alt

# 앱 제목
st.title("지각비 시각화")

# CSV 파일 경로 설정
csv_path = os.path.join(os.path.dirname(__file__), "data.csv")

# 파일 불러오기
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 출석번호: .0 제거 및 문자열 처리
attendance = df["번호"].astype(str).str.replace(r"\.0$", "", regex=True)

# 지각 횟수 처리 (D열 = index 3)
lateness = df.iloc[:, 3].fillna(0).astype(int)

# 💰 금액 컬럼 클린업 함수 (숫자 외 값도 처리)
def clean_money(series):
    return (
        pd.to_numeric(
            series.astype(str)
            .str.replace(r"[₩원,\s]", "", regex=True)
            .replace("", "0"),
            errors="coerce"  # 숫자로 변환 안 되면 NaN
        ).fillna(0).astype(int)  # NaN을 0으로
    )

# 정제된 금액 데이터
paid = clean_money(df["지불비용"])
unpaid = clean_money(df["남은금액"])
total = clean_money(df["총액"])


# 금액 컬럼 정제
paid = clean_money(df["지불비용"])
unpaid = clean_money(df["남은금액"])
total = clean_money(df["총액"])

# 시각화용 데이터프레임 생성 (합계 행 제외)
plot_df = pd.DataFrame({
    "출석번호": attendance,
    "이름": df["이름"],
    "지각 횟수": lateness,
    "총액": total,
    "지불비용": paid,
    "남은금액": unpaid
}).iloc[:32]

# 미납 여부 컬럼 추가 (True = 아직 안 낸 금액 있음)
plot_df["미납"] = plot_df["남은금액"] > 0

# 출석번호 정렬 기준 리스트
domain_list = plot_df["출석번호"].tolist()

# Altair 색상 맵 정의 (납부완료: 파랑 / 미납: 빨강)
color_scale = alt.Scale(
    domain=[False, True],
    range=["#4B9CD3", "#FF6B6B"]
)

# Altair 그래프 생성
chart = (
    alt.Chart(plot_df)
    .mark_bar()
    .encode(
        x=alt.X("지각 횟수:Q", title="지각 횟수", axis=alt.Axis(format="d", tickMinStep=1)),
        y=alt.Y("출석번호:O", title="출석번호", scale=alt.Scale(domain=domain_list),
                axis=alt.Axis(labelOverlap=False)),
        color=alt.Color("미납:N", scale=color_scale, legend=alt.Legend(title="미납 여부")),
        tooltip=["이름", "지각 횟수", "총액", "지불비용", "남은금액"]
    )
    .properties(width=700, height=len(domain_list) * 25)
)

# 그래프 출력
st.altair_chart(chart, use_container_width=True)

# 지각비 총액 출력 (CSV의 마지막 행 기준 남은금액)
try:
    raw_value = df.at[32, "남은금액"]
    cleaned_value = str(raw_value).replace("₩", "").replace(",", "").strip()
    total_fee = int(cleaned_value)
    st.markdown(f"### 💰 현재 지각비 총액: {total_fee:,}원")
except Exception as e:
    st.error(f"❌ 지각비 총액을 불러올 수 없습니다.\n오류: {e}")
