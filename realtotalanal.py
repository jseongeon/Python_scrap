import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

# 한글 폰트 설정
rc('font', family='Pretendard')

# 데이터 정의
월 = ['10월', '11월', '12월', '1월']
발행량 = np.array([300, 306, 232, 395])
유입량 = np.array([361, 373, 334, 271])
전환율 = (유입량 / 발행량) * 100  # 전환율 (%) 계산

# 1. 막대 + 선 그래프 생성
fig, ax1 = plt.subplots(figsize=(29, 27))

x = np.arange(len(월))  # X축 위치

# 막대 그래프 (유입량 & 발행량)
bar_width = 0.4
bars1 = ax1.bar(x - bar_width/2, 유입량, bar_width, color='red', alpha=0.7, label='유입량')
bars2 = ax1.bar(x + bar_width/2, 발행량, bar_width, color='blue', alpha=0.7, label='발행량')

# 막대 그래프 위에 숫자 표시
for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 7, f'{int(bar.get_height())}', 
             ha='center', fontsize=20, fontweight='bold', color='red')
for bar in bars2:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 7, f'{int(bar.get_height())}', 
             ha='center', fontsize=20, fontweight='bold', color='blue')

ax1.set_ylabel('건수', fontsize=12, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(월, fontsize=12, fontweight='bold')

# 선 그래프 (전환율)
ax2 = ax1.twinx()
line, = ax2.plot(x, 전환율, color='#1BD09F', marker='o', linestyle='-', linewidth=2, markersize=8, label='전환율 (%)')

# 전환율 데이터 표시 (텍스트 위로 조정)
for i, txt in enumerate(전환율):
    ax2.text(x[i], 전환율[i] - 3.3, f'{txt:.2f}%', ha='center', fontsize=20, fontweight='bold', color='black')

ax2.set_ylabel('전환율 (%)', fontsize=20, fontweight='bold', color='green')

# 모든 범례를 하나로 합침
lines = [line]
labels = ['전환율 (%)']
bars = [bars1.patches[0], bars2.patches[0]]
labels += ['유입량', '발행량']
legend_elements = lines + bars
ax1.legend(legend_elements, labels, loc='upper left')

# 타이틀 설정
plt.title('블로그 발행량 & 유입량 대비 전환율', fontsize=14, fontweight='bold')

# 저장
output_image_path = "C:/Users/thr_l/OneDrive/바탕 화면/정성언/22_DATA/conversion_rates_chart.png"
plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"이미지가 저장되었습니다: {output_image_path}")


# 2. 원형 차트 (전환율 비율)
fig, ax = plt.subplots(figsize=(7, 7))
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
plt.pie(전환율, labels=월, autopct=lambda p: f'{p:.1f}%\n({p * sum(전환율) / 100:.2f}%)', 
        startangle=90, colors=colors, textprops={'color': 'black', 'fontweight': 'bold'})

# 제목 설정
plt.title('월별 전환율 비율', fontsize=14, fontweight='bold')

# 저장
output_image_path = "C:/Users/thr_l/OneDrive/바탕 화면/정성언/22_DATA/conversion_rates_chart.png"
plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"이미지가 저장되었습니다: {output_image_path}")

