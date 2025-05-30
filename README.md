# 🛍️Shopping Mood  
“소비자의 쇼핑 기분, 데이터로 들여다보다”  
서울 주요 백화점 방문 데이터를 기반으로 한 소비 트렌드 분석 Streamlit 앱  

## 📌프로젝트 개요  
신세계 강남, 롯데 본점, 여의도 더현대의 방문 데이터를 바탕으로  
월별 방문 추이, 계절별 트렌드, 주거지/근무지 기반 방문 비율을 시각화하여  
소비자의 행동 패턴과 마케팅 인사이트를 도출하기 위한 데이터 분석 도구입니다.  

## 🛠️사용 기술 스택  

| 구분           | 기술                                      |
| ------------ | --------------------------------------- |
| 데이터 웨어하우스 | `Snowflake` (Marketplace + Snowpark 활용) |
| 데이터 처리    | `SQL`, `pandas`                         |
| 웹 앱 프레임워크 | `Streamlit`                             |
| 시각화       | `Plotly Express`                        |
| 분석 주제     | 유동인구, 기후, 소비 연계 분석                      |
| 기타        | 한글 폰트 커스터마이징, 사이드바 기반 인터랙션 UI           |

## 주요 시각화 정보  
1. 📈 월별 방문자 추이  
- 백화점별 월간 방문자 수 시계열 분석  
- 연말 특수 / 방학 시즌 등 특정 시점에서의 방문 급증 포착
  
2. 🌸 계절별 방문자 수  
- 봄, 여름, 가을, 겨울로 그룹핑한 계절별 트렌드 분석
- 계절별 특수, 외부 환경(날씨/이벤트)의 영향 분석
- 각 백화점의 공간 특성과 정체성 연결

3. 🏠/🏢 지역별 방문 비율
- 주거지 vs 근무지 기반 방문자 분포 분석
- 각 백화점이 어떤 지역 기반 고객층에 영향을 미치는지 시각화
- "직장 근처 소비", "지역 충성도", "균형 잡힌 유입" 등의 패턴 파악

## 💡구현 포인트 & 인사이트
- Snowflake SQL View로 사전 데이터 정제 후 pandas에서 후처리  
→ 분석 단계에서의 유연성과 속도 확보  

- 월(MONTH) 데이터를 계절 정보로 변환  
→ 계절별 이용자 코호트 분석  

- Streamlit의 사이드바, 멀티셀렉트, 라디오 버튼 등을 이용해 사용자 선택 기반 시각화 구현
- Plotly를 활용한 라인/막대 차트로 깔끔한 UX 제공 + 한글 폰트 이슈 해결
- 정성적 분석 마크다운을 함께 삽입하여, 데이터 읽기의 목적성을 강화
→ 데이터 비친화 유저 UX 고려

## 느낀 점 & 회고

### 🎓인문학적 관점 - "숫자 너머의 맥락 읽기"
이번 프로젝트는 단순한 방문자 수의 시각화에 그치지 않고,  
"왜 이 시점에 사람들이 이 공간에 모였을까?",  
"소비자들이 진짜 원하는 건 쇼핑일까, 경험일까?"  
라는 질문으로 확장되었다.  

특히 흥미로웠던 것은  
단순히 방문자 수가 많다고 해서 그 공간이 '성공적인 소비 공간'으로 해석되지는 않는다는 점이다.  
예: 여의도 더현대의 8월 상승 → 실내 피서처로서의 역할, 신세계 강남의 계절 불문 유입 → 브랜드, 업무 접근성과 같은 구조적 요인  
이런 해석은 단순한 숫자만으로는 설명되지 않는다.  

데이터는 항상 '의미'를 요구한다.  
숫자 자체보다, 그 숫자를 둘러싼 맥락과 사용자의 행위 배경을 읽는 게 중요했다.  
'방문자 수'라는 지표는 마케팅이나 공간 기획의 기준이 될 수는 있지만,  
궁극적으로는 방문자가 지갑을 여는지,  
그 경험이 브랜드와 연결되는지가 핵심이다. 단순 숫자를 늘리는 게 아니라  
맥락과 배경을 파악한 핵심 유저를 확보하는 것이 더 중요할 것이다.  

이번 프로젝트를 통해 데이터는 설득력 있는 이야기를 만들기 위한 재료일 뿐이며,  
그 이야기를 설계하는 능력은 인문학적 통찰에서 비롯된다는 걸 확신했다.  

### ⚙️기술적 관점 – "분석은 구조에서 시작된다"
개발자로서 가장 많이 느낀 건,  
분석을 시작하기 전에 다양한 변수를 고려한 활용 기술 스택 계획,   
데이터의 구조와 흐름을 설계하는 일이 매우 중요하다는 것이다.  

Snowflake market에서 받은 데이터를 Streamlit에서 바로 보여주면 되겠지? 싶었는데,  
권한 문제도 발생했고, 테이블 간 연관성을 만드는데부터 어려움을 겪었다.  
그래서 SQL View를 통해 필요한 컬럼을 정제하고 데이터 구조 전처리를 시행했다.  
그러나 분석 중에 새로운 컬럼이 필요해지고, 필터링 해야하는 일이 생기면서 전처리에 부족함이 많았음을 깨달았다.  
해결을 위해 데이터 구조를 처음부터 다시 잡고 시작하기에는 시간과 능력이 부족했다.  
그래서 데이터 추가, 수정이 용이한 pandas를 필터링, 계절 컬럼 생성 등에 활용했다.  
결론적으로 분석 목적을 분명하게 하고 데이터 구조 설게, 전처리를 꼼꼼하게 해두는 것이 정말 중요하다고 느꼈다.  

시각화를 위해 기존에 사용해본 적 있는 Matplotlib으로 시작했으나 한글 폰트 깨짐 이슈가 있었다.  
이를 해결하기 위해 Plotly로 전환하면서,  
color_discrete_map, category_orders 등을 활용해  
브랜드 컬러와 UX를 의식한 데이터 표현 방식을 배웠다.  
특히 데이터 비친화적 유저에게 디자인적 요소가 없는 데이터는  
아무런 의미가 없을 수 있겠다고 생각했다.  
그래서 단순히 보기 좋은 시각화를 넘어서  
데이터의 흐름과 사용자의 해석을 자연스럽게 유도하는 시각화 구조를 고민하게 되었다.  

계획에 없던 pandas 사용, Matplotlib에서 Plotly로 전환한 경험은  
기술, 라이브러리 공부에는 '목적'이 있어야 한다는 것을 깨닫게 만들어줬다.  
학습 목적을 명확하게 하고 활용할 수 있는 상황을 상정하고 경험해봐야,  
분석, 개발 상황에서 생기는 다양한 변수나 오류에 적절히 활용할 수 있겠다고 체감했다.  


## 개선방향
### '무엇을' 분석하고, 보여주는지보다 '왜' 분석하고, '어떻게' 보여줄 것인지 고민해야 한다.
해당 프로젝트는 snowflake와 streamlit 학습을 위한 기초적인 수준에서 진행됐다.  
부족한 기술 스택으로 인해 좋은 데이터를 시각화하기에 급급해 놓친 부분이 많아 아쉽다.  
다음 프로젝트에서는 좀 더 많은 시간을 두고 '인문학적 인사이트 도출'(기획)에 더 많은 노력을 쏟고,  
시각화 방법도 더 다양하게 테스트하고 피드백 받고 싶다.  
