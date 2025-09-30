import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 1학년 학생 비만/저체중 분포 분석")

# 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])
if uploaded_file:
    # 데이터 불러오기
    df = pd.read_excel(uploaded_file, sheet_name="데이터 엑셀다운")

    # 필요한 열만 추출
    df_bmi = df[["학년", "반", "성별", "체질량지수_학생", "비만도_학생"]].copy()

    # ==============================
    # 전체 분포 그래프
    # ==============================
    st.subheader("전체 학생 분포")
    counts = df_bmi["비만도_학생"].value_counts().reset_index()
    counts.columns = ["구분", "학생 수"]

    fig1 = px.bar(counts, x="구분", y="학생 수",
                  title="1학년 전체 비만/저체중 분포",
                  text="학생 수")
    st.plotly_chart(fig1)

    # ==============================
    # 학급별 분포 그래프 (비율 기준)
    # ==============================
    st.subheader("학급별 분포 비교 (비율 %)")

    class_counts = df_bmi.groupby(["반", "비만도_학생"]).size().reset_index(name="학생 수")
    # 각 반별 합계 구해서 비율로 변환
    class_counts["비율(%)"] = class_counts.groupby("반")["학생 수"].transform(lambda x: x / x.sum() * 100)

    fig2 = px.bar(class_counts, 
                  x="반", y="비율(%)", color="비만도_학생", 
                  title="1학년 학급별 비만/저체중 분포 (%)",
                  text=class_counts["비율(%)"].round(1),
                  barmode="stack")
    st.plotly_chart(fig2)

    # ==============================
    # 원시 데이터 미리보기
    # ==============================
    with st.expander("📑 원본 데이터 미리보기"):
        st.dataframe(df_bmi.head(20))
else:
    st.info("왼쪽에 있는 '엑셀 파일 업로드' 버튼을 이용해 데이터를 불러오세요.")
