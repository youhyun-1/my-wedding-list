import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="나의 축의금 장부", layout="wide")

st.title("🧧 모바일 축의금 검색 프로그램")
st.info("바탕화면의 엑셀 파일을 아래에 업로드하면 바로 조회가 가능합니다.")

# 1. 파일 업로드
uploaded_file = st.file_uploader("축의금 정리.xlsx 파일을 선택하세요", type=['xlsx', 'csv'])

if uploaded_file:
    # 데이터 읽기
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # 컬럼명 정리 및 4번 칼럼까지만 추출
        df.columns = [str(c).strip() for c in df.columns]
        df_display = df.iloc[:, :4] 
        
        # 금액 컬럼 숫자화 (사용자 파일 기준: '축의금 금액 (원)')
        money_col = '축의금 금액 (원)'
        if money_col in df_display.columns:
            df_display[money_col] = pd.to_numeric(df_display[money_col], errors='coerce').fillna(0).astype(int)

        # 2. 상단 통계 카드
        total_people = len(df_display[df_display[money_col] > 0])
        total_sum = df_display[money_col].sum()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("총 인원", f"{total_people} 명")
        with col2:
            st.metric("총 금액", f"{total_sum:,} 원")

        # 3. 검색 기능
        search_term = st.text_input("🔍 이름이나 소속을 입력하여 검색하세요 (예: 부모님, 서유현)")

        if search_term:
            mask = df_display.apply(lambda row: row.astype(str).str.contains(search_term).any(), axis=1)
            filtered_df = df_display[mask]
        else:
            filtered_df = df_display

        # 4. 결과 표 출력 (오름차순/내림차순 정렬 자동 지원)
        st.write(f"검색 결과: {len(filtered_df)}건")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
else:
    st.warning("파일을 업로드해 주세요.")