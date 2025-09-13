import streamlit as st
import pandas as pd
import altair as alt
import os

# 제목
st.title("🌍 국가별 MBTI 유형 분포 분석")

# CSV 파일 기본 경로
default_file = "countriesMBTI_16types.csv"

# 데이터 불러오기
df = None
if os.path.exists(default_file):
    df = pd.read_csv(default_file)
else:
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

# 데이터가 준비된 경우
if df is not None:
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

    # Altair 그래프
    chart = (
        alt.Chart(top10)
        .mark_bar()
        .encode(
            x=alt.X(selected_type, title="비율"),
            y=alt.Y("Country", sort="-x", title="국가"),
            tooltip=["Country", selected_type],
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

else:
    st.warning("CSV 파일을 찾을 수 없습니다. 업로드해주세요.")
