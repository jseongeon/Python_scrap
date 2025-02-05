import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_conversion_chart(data, output_path):
    # 데이터프레임 생성 (NaN을 0으로 채운 후 정수형 변환)
    df = pd.DataFrame.from_dict(data, orient="index").fillna(0).astype(int)

    # 시도 건수, 전환 건수 뒤에 "건" 추가
    df["시도 건수"] = df["시도 건수"].astype(str) + "건"
    df["전환 건수"] = df["전환 건수"].astype(str) + "건"

    # 전환율 계산 (100을 곱해 올바르게 계산)
    df["전환율 (%)"] = (
        df["전환 건수"].str.replace("건", "").astype(float) / 
        df["시도 건수"].str.replace("건", "").astype(float)
    ) * 100  # 100 곱하기 추가

    df["전환율 (%)"] = df["전환율 (%)"].replace([float('inf'), -float('inf')], 0).round(2)  # 무한대 방지 및 반올림

    # 한글 폰트 설정
    plt.rc('font', family='Pretendard')

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis('tight')
    ax.axis('off')

    # 테이블 생성
    table = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, 
                     cellLoc='center', loc='center', colColours=["lightgray"]*3)

    # 전환율(%) 제목을 빨간색으로 설정
    table[0, 2].set_text_props(color='red', fontweight='bold')

    # 전환율 데이터 볼드체 설정
    for i in range(1, len(df) + 1):
        table[i, 2].set_text_props(fontweight='bold')
    
    # 총합 행 볼드체 및 빨간색 적용
    total_row = len(df)
    for j in range(len(df.columns)):
        table[total_row, j].set_text_props(color='red', fontweight='bold')

    # 디렉토리 확인 및 생성
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # 이미지 저장
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"이미지가 저장되었습니다: {output_path}")
    return output_path

# 샘플 데이터
data = {
    "GEM": {"시도 건수": 79, "전환 건수": 64},  # 312.5%로 정상 표시되어야 함
    "WOO": {"시도 건수": 77, "전환 건수": 59},
    "KOO": {"시도 건수": 79, "전환 건수": 40},
    "ICA": {"시도 건수": 32, "전환 건수": 6},
    "JIN": {"시도 건수": 58, "전환 건수": 41},
    "LANG": {"시도 건수": 70, "전환 건수": 61},
    "총합": {"시도 건수": 395, "전환 건수": 271}
}

# 실행 및 저장
output_image_path = "C:/Users/thr_l/OneDrive/바탕 화면/정성언/22_DATA/conversion_rates_chart.png"
generate_conversion_chart(data, output_image_path)
