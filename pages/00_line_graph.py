import os
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.title("지각 횟수 돌림판")

# ── 1) 데이터 준비 ─────────────────────────────────────
csv_path = os.path.join(os.path.dirname(__file__), "../data.csv")
df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 지각 횟수 정제 (D열 기준)
df["지각 횟수"] = df.iloc[:, 3].fillna(0).astype(int)

# 상위 10명 + 기타 그룹 생성
top10 = df.nlargest(10, "지각 횟수")[["이름", "지각 횟수"]]
others = df[~df["이름"].isin(top10["이름"])]
others_sum = pd.DataFrame([{
    "이름": "기타",
    "지각 횟수": int(others["지각 횟수"].sum())
}])
final_df = pd.concat([top10, others_sum], ignore_index=True)

labels = list(final_df["이름"])
values = list(final_df["지각 횟수"])

# ── 2) Chart.js 돌림판 HTML ────────────────────────────
html = f"""
<canvas id="wheel" width="400" height="400"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const ctx = document.getElementById('wheel').getContext('2d');
const data = {{
  labels: {labels},
  datasets: [{{
    data: {values},
    backgroundColor: [
      '#3366cc','#dc3912','#ff9900','#109618','#990099',
      '#0099c6','#dd4477','#66aa00','#b82e2e','#316395','#954535'
    ]
  }}]
}};
const config = {{
  type: 'pie',
  data: data,
  options: {{
    responsive: false,
    animation: false,
    plugins: {{
      tooltip: {{ enabled: true }}
    }}
  }}
}};
const wheel = new Chart(ctx, config);

// 클릭할 때마다 무작위 회전
ctx.canvas.addEventListener('click', () => {{
  const angle = Math.random() * 360;
  wheel.options.rotation = angle * Math.PI / 180;
  wheel.update();
}});
</script>
"""

# ── 3) Streamlit에 포함 ──────────────────────────────────
components.html(html, height=450)
