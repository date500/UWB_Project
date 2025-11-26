import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os

def calculate_parameters():
    filename = 'All_data.csv'

    # 1. 파일이 있는지 확인
    if not os.path.exists(filename):
        print(f"오류: '{filename}' 파일을 찾을 수 없습니다.")
        return

    # 2. CSV 파일 읽기
    # 파일 구조: 실제거리, 각도, 측정값
    try:
        df = pd.read_csv(filename, header=None, names=['실제거리', '각도', '측정값'])
        print(f"['{filename}'] 파일 로드 성공! (데이터 {len(df)}개)")
    except Exception as e:
        print(f"파일 읽기 오류: {e}")
        return

    # -------------------------------------------------------------------------
    # 3. 데이터 전처리 (Degree -> Radian 변환)
    # 공식: Radian = Degree * (π / 180)
    # -------------------------------------------------------------------------
    # '각도' 컬럼을 가져와서 라디안으로 변환하여 새로운 컬럼 '각도_rad'에 저장
    df['각도_rad'] = df['각도'] * (np.pi / 180)

    # -------------------------------------------------------------------------
    # 4. 학습 데이터 준비
    # -------------------------------------------------------------------------
    # X (독립변수): [실제거리, 각도(rad)]
    X = df[['실제거리', '각도_rad']]
    
    # y (종속변수): [측정값]
    y = df['측정값']

    # -------------------------------------------------------------------------
    # 5. 회귀분석 (최소자승법) 수행
    # -------------------------------------------------------------------------
    model = LinearRegression()
    model.fit(X, y)

    # 계수 추출
    a1 = model.coef_[0]      # 실제거리의 계수
    a2 = model.coef_[1]      # 각도(rad)의 계수
    a3 = model.intercept_    # 상수항 (절편)

    # -------------------------------------------------------------------------
    # 6. 결과 출력
    # -------------------------------------------------------------------------
    print("\n" + "="*40)
    print(" 분석 결과 (Radian 기준)")
    print("="*40)
    print(f" a_1 (거리 계수) : {a1:.6f}")
    print(f" a_2 (각도 계수) : {a2:.6f}")
    print(f" a_3 (상수항)   : {a3:.6f}")
    print("-" * 40)
    print(" [최종 공식]")
    print(f" 측정값 = 실제거리 * ({a1:.5f}) + 각도(rad) * ({a2:.5f}) + ({a3:.5f})")
    print("="*40)
    
    # 검증용: 첫 번째 데이터로 계산해보기
    test_dist = df.iloc[0]['실제거리']
    test_deg = df.iloc[0]['각도']
    test_rad = df.iloc[0]['각도_rad']
    test_real = df.iloc[0]['측정값']
    
    calc_val = (test_dist * a1) + (test_rad * a2) + a3
    print(f"\n[검증] 첫 번째 데이터 (거리:{test_dist}m, 각도:{test_deg}도)")
    print(f" - 실제 측정값 : {test_real}")
    print(f" - 공식 계산값 : {calc_val:.6f}")
    print(f" - 오차       : {abs(test_real - calc_val):.6f}")

if __name__ == "__main__":
    calculate_parameters()