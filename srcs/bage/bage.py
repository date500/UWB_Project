import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 파일 및 설정
# ==========================================
FILE_NAME = '1m_30deg.csv'  # 분석할 데이터 파일
BASELINE = 2048             # 센서 베이스라인 값
MAX_TIME_SEC = 35.0         # 세로축: 시간 (초)
MAX_DIST_METER = 5.0        # 가로축: 거리 (미터)

# ==========================================
# 2. 데이터 로드
# ==========================================
try:
    df = pd.read_csv(FILE_NAME, header=None, sep=',')
    num_rows, num_cols = df.shape
    print(f"✅ 데이터 로드 성공: {num_rows}행 x {num_cols}열")
except FileNotFoundError:
    print(f"❌ 오류: '{FILE_NAME}' 파일을 찾을 수 없습니다.")
    exit()

# ==========================================
# 3. 데이터 가공 (명암비 강조 및 확률 변환)
# ==========================================
# (1) 에너지 계산: 베이스라인 제거를 통해 순수 신호 추출
energy_map = np.abs(df.values - BASELINE)

# (2) ★핵심★: 명암 대비(Contrast) 극대화 (Robust Scaling)
# 상위 0.5% 값을 최대 밝기 기준으로 설정하여 이상치(Outlier)에 의한 시각화 왜곡 방지
v_max_limit = np.percentile(energy_map, 99.5) 
if v_max_limit == 0: v_max_limit = 1 # 에러 방지용 안전장치

# (3) 확률 분포 변환 (Probability Map)
# 전체 에너지 합으로 나누어 '존재 확률'로 정규화
prob_map = energy_map / np.sum(energy_map)

# ==========================================
# 4. 고해상도 시각화
# ==========================================
plt.figure(figsize=(10, 12))

# (1) 메인 히트맵 (Turbo Colormap 적용)
plt.imshow(energy_map, 
           aspect='auto', 
           cmap='turbo', 
           interpolation='bilinear',  # 부드러운 픽셀 처리
           vmax=v_max_limit,          # 명암비 최적화 적용
           extent=[0, MAX_DIST_METER, MAX_TIME_SEC, 0]) 

plt.colorbar(label='Signal Intensity (High Contrast)')

# (2) 등고선(Contour) 추가 - 확률이 높은 핵심 구역 표시
x = np.linspace(0, MAX_DIST_METER, num_cols)
y = np.linspace(0, MAX_TIME_SEC, num_rows)
X, Y = np.meshgrid(x, y)

plt.contour(X, Y, prob_map, 
            levels=5, 
            colors='white', 
            alpha=0.3, 
            linewidths=0.5)

# (3) 라벨링 및 그리드
plt.xlabel("Distance (m) ->", fontsize=12, fontweight='bold')
plt.ylabel("Time (sec) ↓", fontsize=12, fontweight='bold')
plt.title(f"Enhanced Range-Time Map: {FILE_NAME}", fontsize=14)

plt.grid(color='white', linestyle=':', linewidth=0.5, alpha=0.4)
plt.xticks(np.arange(0, MAX_DIST_METER + 1, 1.0))
plt.yticks(np.arange(0, MAX_TIME_SEC + 1, 5.0))

plt.tight_layout()
plt.show()