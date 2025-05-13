import streamlit as st
import plotly.express as px
import pandas as pd
from snowflake.snowpark.context import get_active_session

#세션 연결
session = get_active_session()

#데이터 불러오기
department_visit_df = session.table("DEPARTMENT_STORE_DATA_VIEW").to_pandas()
floating_df = session.table("FLOATING_POPULATION_INFO_VIEW").to_pandas()
home_df = session.table("HOME_OFFICE_RATIO_VIEW").to_pandas()

#계절 컬럼 생성
def get_season(mm):
    mm = int(mm)
    if mm in [3, 4, 5]:
        return "봄"
    elif mm in [6, 7, 8]:
        return "여름"
    elif mm in [9, 10, 11]:
        return "가을"
    else:
        return "겨울"

department_visit_df["season"] = department_visit_df["MONTH"].astype(int).apply(get_season)

#사이드바 메뉴
st.sidebar.header("📍 메뉴 선택")
page = st.sidebar.radio("📊 보고 싶은 항목을 선택하세요", ["📈 월별 방문자 추이", "🌸 계절별 방문자 수", "🏠/🏢 지역별 방문 비율"])

#백화점 선택 필터
dep_options = department_visit_df["DEP_NAME"].unique().tolist()
selected_dep = st.sidebar.multiselect("🏬 백화점 선택", dep_options, default=dep_options)
filtered_df = department_visit_df[department_visit_df["DEP_NAME"].isin(selected_dep)]

#월별 요약
monthly_df = filtered_df.groupby(["YEAR_MONTH", "DEP_NAME"])["COUNT"].sum().reset_index()

#계절별 요약
season_df = filtered_df.groupby(["season", "DEP_NAME"])["COUNT"].sum().reset_index()

#페이지 구성
if page == "📈 월별 방문자 추이":
    st.subheader("📈 월별 방문자 추이")
    fig1 = px.line(
        monthly_df,
        x="YEAR_MONTH", y="COUNT", color="DEP_NAME", markers=True,
        title="백화점별 월간 방문 추이",
        labels={"YEAR_MONTH": "월", "COUNT": "방문자 수", "DEP_NAME": "백화점"},
        color_discrete_map={
            "신세계 강남": "#3498db",
            "롯데 본점": "#2ecc71",
            "여의도 더현대": "#e74c3c"
        }
    )
    fig1.update_layout(template="plotly_white", xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    ### 주요 분석 결과

    **1️⃣ 신세계 강남**  
    - 연중 방문자 수 가장 높음 → 브랜드/접근성/업무 밀집 영향
    - 구매력 있는 타깃층 **상시 유입 가능성**이 큼
    - 쇼핑이라는 근본 백화점 역할 수행  
    -> 체류시간 늘리기 보다 동선최적화 등을 통한 고객 불편 해소
    
    **2️⃣ 롯데 본점 & 여의도 더현대 (연말 특수)**  
    - 11월부터 방문객 급증 → 크리스마스 콘텐츠 및 관광요소 작용
    - 명동에 위치해 외국인 관광객 많은 롯데 본점 
    - 장소 마케팅으로 성장한 여의도 더현대

    **3️⃣ 여의도 더현대 (8월 이례적 상승)**  
    - 방학 특수로 인한 실내 피서처 수요 + 문화적 공간 경험 확대

    ### 💡 인사이트 제안
    > **시간 보내기 좋은 공간**과 **쇼핑을 위한 공간** 중 하나에 집중해 정체성을 강화해야한다.   
    > 높은 방문자 수가 항상 높은 매출로 이어지는 것은 아니다. 정체성에 맞는 품목 구성이 동반 되어야한다.
    > 결국 방문자들이 지갑을 열게 만드는 BM 설정이 핵심 과제이다.
    """)
    
elif page == "🌸 계절별 방문자 수":
    st.subheader("🌸 계절별 방문자 수 비교")
    fig2 = px.bar(
        season_df,
        x="season", y="COUNT", color="DEP_NAME", barmode="group",
        title="계절별 백화점 방문자 수",
        labels={"season": "계절", "COUNT": "방문자 수", "DEP_NAME": "백화점"},
        category_orders={"season": ["봄", "여름", "가을", "겨울"]},
        color_discrete_map={
            "신세계 강남": "#3498db",
            "롯데 본점": "#2ecc71",
            "여의도 더현대": "#e74c3c"
        }
    )
    fig2.update_layout(template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    ### 🍂 주요 분석 결과
    
    ---
    
    **1️⃣ 전체 백화점 공통 특징**  
    - **겨울(12월)** 방문자 수가 가장 많음  
      → **연말 시즌 특수 효과**    
      → 가족 단위 방문 및 데이트 수요 증가로 해석 가능  
    
    ---
    
    **2️⃣ 신세계 강남**  
    - 계절에 크게 흔들리지 않고 **안정적인 방문자 수 유지**  
    - 백화점의 ‘기본 기능’(쇼핑 편의성, 입점 브랜드, 교통 접근성 등)이 충실한 대표 사례  
    → 계절 마케팅 없이도 **고정 수요층**이 지속 유입되고 있음을 보여줌  
    
    ---
    
    **3️⃣ 롯데 본점**  
    - **겨울 시즌(11~12월)** 뚜렷한 상승  
      → 명동 및 관광객 유입 증가 + 크리스마스 시즌 특수  
      → ‘포토존’ 및 ‘분위기 소비’ 요소가 방문 결정에 영향  
      → **외국인 관광 수요**가 특히 반영될 수 있음  
    
    ---
    
    **4️⃣ 여의도 더현대 – 가을 급락 원인**  
    - **가을(9~10월) 방문자 수가 이례적으로 낮음**  
      → 추석 등 연휴가 포함된 시기로 **도심 내 활동 수요 감소** 가능성  
      → 타 계절에 비해 **대형 전시/이벤트 비중이 상대적으로 적었던 기간**  
      → 가을철 날씨가 좋아 실외 활동 선호가 증가하면서 실내 쇼핑 비중 감소로 해석 가능  
    
    ---
    
    **💡 인사이트 제안**  
    > “방문자 수는 단순 계절이 아닌, 그 계절에 어떤 콘텐츠와 경험이 제공되느냐에 따라 달라진다.  
    > 특히 연말·겨울철 백화점 방문은 쇼핑보다 ‘분위기 소비’를 향한 수요가 강하게 반영된다.  
    > 따라서 **이벤트/공간기획 전략**이 방문자 유입의 핵심 포인트임을 고려할 필요가 있다.”
    """)


elif page == "🏠/🏢 지역별 방문 비율":
    st.subheader("🏠/🏢 지역별 백화점 방문 비율")

    #LOC_TYPE 라벨링 (1=주거지, 2=근무지)
    home_df["LOC_TYPE_LABEL"] = home_df["LOC_TYPE"].map({1: "주거지", 2: "근무지"})

    #선택 필터
    loc_type = st.radio("🏠/🏢 주거지 or 근무지", ["주거지", "근무지"])

    #필터링된 데이터
    filtered_home = home_df[home_df["LOC_TYPE_LABEL"] == loc_type]

    #지역별 백화점 방문 비율 요약
    summary_df = (
        filtered_home.groupby(["ADDR_LV2", "DEP_NAME"])["RATIO"]
        .mean()
        .reset_index()
        .sort_values(by="RATIO", ascending=False)
    )

    #시각화
    fig3 = px.bar(
        summary_df,
        x="ADDR_LV2",
        y="RATIO",
        color="DEP_NAME",
        barmode="group",
        title=f"{loc_type} 기준 지역별 백화점 방문 비율",
        labels={"ADDR_LV2": "행정구", "RATIO": "평균 방문 비율", "DEP_NAME": "백화점"},
        template="plotly_white"
    )
    fig3.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    ### 주요 분석 결과
    
    ---
    
    **1️⃣ 근무지 기준 → 모든 백화점 공통 특징**  
    - **세 백화점 모두** 해당 백화점이 위치한 **행정구 근무지에서의 방문률이 압도적으로 높음**  
    - 백화점 소비는 **업무와 연결된 짧은 체류 소비 패턴**과 밀접한 관계  
    → 업무 시간 전후, 점심시간 등 **틈새 시간 소비층 확보**에 효과적
    
    ---
    
    **2️⃣ 신세계 강남 → 고소득 상권과의 강한 연계**  
    - **서초구, 강남구** 등지에서 **주거지 기준** 방문률도 매우 높음  
    - 해당 지역의 **고소득·고연령 소비자층 충성도** 반영  
    - **직주근접 쇼핑 수요 + 브랜드 중심 소비 성향**이 결합된 결과
    
    ---
    
    **3️⃣ 롯데 본점 → 강북권에서의 상대적 강세**  
    - **중구에 위치**, 근무지 기준으로는 방문률이 압도적  
    - **주거지 기준**으로 보면, **도봉구·강북구·은평구 등 북부 지역**에서의 방문 비율이 비교적 높게 나타남  
    → 도심 접근성과 더불어 **중저가 쇼핑 수요** 및 **관광·문화 연계 수요**가 결합된 패턴
    
    ---
    
    **4️⃣ 여의도 더현대 → 완만하지만 서울 전역 유입**  
    - 근무지 기준에서는 **영등포구**에서 방문률이 높게 나타남  
    - **주거지 기준**으로 보면 일부 지역 편향은 있으나,  
      → **서울 전역에서 고르게 방문**하는 특징  
    - **콘텐츠 중심 복합문화공간**으로서의 인식  
    → **체험·가족 단위** 방문이 다른 백화점보다 상대적으로 높은 비중을 차지할 가능성
    
    ---
    
    ### 💡 종합 인사이트
    > “백화점 소비는 단순한 거리 개념이 아니라,  
    > **생활 반경과 소비 목적에 따라 선택되는 공간**임을 확인할 수 있다.  
    > 각 백화점은 ‘위치 기반’이 아닌 **방문자 유형 기반**의 기획 전략이 요구되며,  
    > **정서적 경험**과 **콘텐츠 공간성**의 경쟁력이 중요한 변수로 작용한다.”
    """)

