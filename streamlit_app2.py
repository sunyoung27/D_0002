import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("per-capita-co-emissions.csv")
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    df = df.rename(columns={'Country', 'year': 'Year', 'co2_per_capita': 'CO2_per_Capita'})
    return df

df = load_data()

# 제목
st.title("🌍 Per Capita CO₂ Emissions Dashboard")
st.markdown("📊 **국가별 1인당 CO₂ 배출량 데이터를 시각화한 대시보드입니다.**")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["세계 지도", "상위 10개국", "상관관계 분석"])

# 🌐 탭1: 세계 지도 시각화
with tab1:
    st.subheader(" 연도별 국가별 1인당 CO₂ 배출량")
    years = sorted(df['Year'].unique(), reverse=True)
    selected_year = st.selectbox("연도 선택", years)
    df_year = df[df['Year'] == selected_year]

    fig_map = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="CO2_per_Capita",
        hover_name="Country",
        color_continuous_scale="YlOrRd",
        title=f"{selected_year}년 국가별 1인당 CO₂ 배출량 (톤)"
    )
    st.plotly_chart(fig_map, use_container_width=True)

# 🏆 탭2: 상위 10개국 바 차트
with tab2:
    st.subheader("{selected_year}년 1인당 CO₂ 배출량 상위 10개국")
    top10 = df_year.sort_values("CO2_per_Capita", ascending=False).head(10)
    fig_bar = px.bar(
        top10,
        x="CO2_per_Capita",
        y="Country",
        orientation="h",
        color="CO2_per_Capita",
        color_continuous_scale="Blues",
        title=f"{selected_year}년 1인당 CO₂ 배출량 상위 10개국"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# 📈 탭3: 상관관계 분석
with tab3:
    st.subheader("변수 간 상관관계 분석")
    numeric_cols = ["CO2_per_Capita", "gdp_per_capita", "population"]

    selected_x = st.selectbox("X축 변수", numeric_cols, index=1)
    selected_y = st.selectbox("Y축 변수", numeric_cols, index=0)

    df_corr = df[df['Year'] == selected_year]
    fig_scatter = px.scatter(
        df_corr,
        x=selected_x,
        y=selected_y,
        text="Country",
        trendline="ols",
        title=f"{selected_x} vs {selected_y} ({selected_year}년)"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

   
