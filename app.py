import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw
import io
from PIL import Image
import base64

# 페이지 설정
st.set_page_config(
    page_title="SMILES 분자 시각화",
    page_icon="🧪",
    layout="wide"
)

# 제목
#st.title("🧪 SMILES 분자 시각화 서비스")

# 사이드바 - SMILES 입력
with st.sidebar:
    st.header("SMILES 입력")
    smiles_input = st.sidebar.text_area(
        "SMILES 문자열을 입력하세요 (한 줄에 하나씩):",
        height=300,
        placeholder="예시:\nCCO\nCCCCCCCCCCCCCCCCCC(=O)O\nC1=CC=CC=C1\nCC(C)CC1=CC=C(C=C1)C(C)C(=O)O"
    )
    
    cols_per_row = st.slider("열 개수", min_value=4, max_value=10, value=6, step=1)

img_width = int(1500/cols_per_row)
img_height = int(img_width*0.67)

# SMILES 문자열 파싱
if smiles_input:
    smiles_list = [smile.strip() for smile in smiles_input.split('\n') if smile.strip()]
else:
    smiles_list = []

# 메인 페이지
if smiles_list:
    st.write(f"총 {len(smiles_list)}개의 분자를 시각화합니다.")

    # 격자 레이아웃을 위한 컬럼 수 설정

    # 분자 시각화
    for i in range(0, len(smiles_list), cols_per_row):
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):
            if i + j < len(smiles_list):
                smiles = smiles_list[i + j]

                with cols[j]:
                    try:
                        # SMILES를 분자 객체로 변환
                        mol = Chem.MolFromSmiles(smiles)

                        if mol is not None:
                            # 분자 이미지 생성
                            img = Draw.MolToImage(mol, size=(img_width, img_height))

                            # 이미지 표시
                            st.image(img, caption=f"{smiles}", use_container_width=False)

                        else:
                            st.error(f"유효하지 않은 SMILES: {smiles}")

                    except Exception as e:
                        st.error(f"오류 발생: {smiles}\n{str(e)}")

else:
    # 안내 메시지
    st.info("👈 사이드바에서 SMILES 문자열을 입력해주세요.")

    # 예시 표시
    st.subheader("사용 예시")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**일반적인 SMILES 예시:**")
        st.code("""CCO (에탄올)
CCCCCCCCCCCCCCCCC(=O)O (스테아르산)
C1=CC=CC=C1 (벤젠)
CC(C)CC1=CC=C(C=C1)C(C)C(=O)O (이부프로펜)
CN1C=NC2=C1C(=O)N(C(=O)N2C)C (카페인)""")

    with col2:
        st.write("**사용 방법:**")
        st.write("1. 왼쪽 사이드바에 SMILES 문자열을 입력합니다")
        st.write("2. 각 줄에 하나의 SMILES를 입력합니다")
        st.write("3. 입력하면 자동으로 분자 구조가 시각화됩니다")

# 사이드바에 추가 정보
st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ 정보")
st.sidebar.write("이 서비스는 RDKit을 사용하여 SMILES 문자열을 분자 구조로 시각화합니다.")
st.sidebar.write("유효하지 않은 SMILES는 오류 메시지가 표시됩니다.")

# 사이드바에 샘플 버튼 추가
if st.sidebar.button("📝 샘플 SMILES 로드"):
    sample_smiles = """CCO
CCCCCCCCCCCCCCCCC(=O)O
C1=CC=CC=C1
CC(C)CC1=CC=C(C=C1)C(C)C(=O)O
CN1C=NC2=C1C(=O)N(C(=O)N2C)C
CC(=O)OC1=CC=CC=C1C(=O)O"""
    st.sidebar.text_area("샘플이 로드되었습니다:", value=sample_smiles, height=200, key="sample")
