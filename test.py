import matplotlib.pyplot as plt
from matplotlib import rc

# 한글 폰트 설정 (Pretendard가 없을 경우 Malgun Gothic 사용)
try:
    rc('font', family='Pretendard')
except:
    rc('font', family='Malgun Gothic')

# 데이터
카테고리 = ['바이럴', '홈페이지', '기타', '추적불가']
문의건수 = [482, 384, 68, 25]
총합 = sum(문의건수)

# 원형 차트 생성
plt.figure(figsize=(7, 7))
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

# 퍼센트와 실제 건수를 함께 표시
plt.pie(문의건수, labels=카테고리, 
        autopct=lambda p: f'{p:.1f}%\n({p * 총합 / 100:.0f}건)', 
        startangle=90, colors=colors, 
        textprops={'color': 'black', 'fontweight': 'bold'})

# 데이터만 빨간색으로 설정
for text in plt.gca().texts:
    if '건' in text.get_text():  # 숫자 값 텍스트만 필터링
        text.set_color('#FF0000')

# 제목 설정
plt.title('문의건 유형별 비율', fontsize=16, fontweight='bold')

# 이미지 저장 및 출력 (변수명 수정)
output_image_path = "C:/Users/thr_l/OneDrive/바탕 화면/정성언/22_DATA/conversion_rates_chart.png"
plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"이미지가 저장되었습니다: {output_image_path}")
