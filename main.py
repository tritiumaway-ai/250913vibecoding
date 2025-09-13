import streamlit as st
import pandas as pd
import altair as alt

# 제목
st.title("🌍 국가별 MBTI 유형 분포 분석")

# CSV 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 데이터 불러오기
    df = pd.read_csv(uploaded_file)

    st.subheader("데이터 미리보기")
    st.dataframe(df.head())

    # MBTI 유형 목록 (첫 번째 컬럼 'Country' 제외)
    mbti_types = df.columns[1:].tolist()

    # 사용자에게 MBTI 유형 선택 받기
    selected_type = st.selectbox("MBTI 유형을 선택하세요", mbti_types)

    # 선택된 MBTI 유형 기준으로 상위 10개국 추출
    top10 = df[["Country", selected_type]].sort_values(
        by=selected_type, ascending=False
    ).head(10)

    st.subheader(f"Top 10 국가 ({selected_type})")

    # Top1 국가명
    top1_country = top10.iloc[0]["Country"]

    # Altair 그래프
    chart = (
        alt.Chart(top10)
        .mark_bar()
        .encode(
            x=alt.X(selected_type, title="비율"),
            y=alt.Y("Country", sort="-x", title="국가"),
            color=alt.condition(
                alt.datum.Country == top1_country,
                alt.value("red"),        # Top1 → 빨간색
                alt.value("steelblue")   # 나머지 → 파란색
            ),
            tooltip=["Country", selected_type],
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

else:
    st.warning("CSV 파일을 업로드해주세요.")
