import streamlit as st
import pandas as pd
import os

# 페이지 설정
st.set_page_config(page_title="나의 축의금 장부", layout="wide")

st.title("🧧 스마트 축의금 장부 (자동 모드)")

# 파일 경로 설정 (GitHub에 같이 올린 파일 이름)
FILE_NAME = "축의금 정리.xlsx"

# 데이터 로드 함수 (캐싱을 통해 속도 향상)
@st.cache_data
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            df = pd.read_excel(FILE_NAME, engine='openpyxl')
            # 컬럼명 앞뒤 공백 제거
            df.columns = [str(c).strip() for c in df.columns]
            return df
        except Exception as e:
            st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
            return None
    else:
        st.error(f"'{FILE_NAME}' 파일을 찾을 수 없습니다. GitHub에 파일을 올렸는지 확인해주세요.")
        return None

df = load_data()

if df is not None:
    # 앞의 4개 컬럼만 선택
    df_display = df.iloc[:, :4]
    
    # 금액 컬럼 숫자 변환 (보내주신 파일 기준: '축의금 금액 (원)')
    money_col = '축의금 금액 (원)'
    if money_col in df_display.columns:
        df_display[money_col] = pd.to_numeric(df_display[money_col], errors='coerce').fillna(0).astype(int)

    # 1. 상단 통계 요약
    total_people = len(df_display[df_display[money_col] > 0])
    total_sum = df_display[money_col].sum()

    col1, col2 = st.columns(2)
    col1.metric("총 인원", f"{total_people} 명")
    col2.metric("총 합계", f"{total_sum:,} 원")

    st.divider()

    # 2. 검색 기능
    search_term = st.text_input("🔍 검색 (이름, 구분, 소속 등 입력)", placeholder="예: 부모님 또는 이름")

    if search_term:
        mask = df_display.apply(lambda row: row.astype(str).str.contains(search_term).any(), axis=1)
        filtered_df = df_display[mask]
    else:
        filtered_df = df_display

    # 3. 결과 출력
    st.subheader(f"조회 결과 ({len(filtered_df)}건)")
    
    # 금액 컬럼에 콤마 표시를 위한 스타일 적용
    st.dataframe(
        filtered_df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            money_col: st.column_config.NumberColumn(format="%d")
        }
    )