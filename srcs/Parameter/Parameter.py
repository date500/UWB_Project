import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def calculate_coefficients():
    filename = '1m_parameter.csv'
    
    try:
        df = pd.read_csv(filename, header=None)
        print(f"'{filename}' 파일을 성공적으로 읽었습니다.")
        print(f"데이터 크기: {df.shape} (행, 열)")
    except FileNotFoundError:
        print(f"오류: '{filename}' 파일을 찾을 수 없습니다. 파일이 같은 폴더에 있는지 확인해주세요.")
        return

    angles = [0, 10, 20, 30] 
    real_distances = np.arange(1, 31) 

    if len(df) != len(real_distances):
        print(f"주의: CSV 데이터 행 개수({len(df)})와 설정한 거리 데이터 개수({len(real_distances)})가 다릅니다.")
        return

    X = []
    y = []

    for row_idx in range(len(df)):
        dist = real_distances[row_idx] # 해당 줄의 실제 거리
        
        for col_idx in range(len(df.columns)):
            # 데이터가 비어있거나 숫자가 아닌 경우 건너뜀 (안전장치)
            val = df.iloc[row_idx, col_idx]
            if pd.isna(val): continue
            
            angle = angles[col_idx]       # 해당 열의 각도
            measured_value = float(val)   # 측정값
            
            X.append([dist, angle])
            y.append(measured_value)

    X = np.array(X)
    y = np.array(y)

    # -------------------------------------------------------------------------
    # 4. 회귀 분석 (계수 계산)
    # -------------------------------------------------------------------------
    model = LinearRegression()
    model.fit(X, y)

    a1 = model.coef_[0]     
    a2 = model.coef_[1]     
    a3 = model.intercept_   

    print("-" * 30)
    print("분석 결과:")
    print(f"a_1 (거리 계수) : {a1:.5f}")
    print(f"a_2 (각도 계수) : {a2:.5f}")
    print(f"a_3 (상수항)   : {a3:.5f}")
    print("-" * 30)
    print("최종 공식:")
    print(f"측정값 = 실제거리 * ({a1:.5f}) + 측정각도 * ({a2:.5f}) + ({a3:.5f})")

if __name__ == "__main__":
    calculate_coefficients()