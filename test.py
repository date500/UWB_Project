import numpy as np

def calculate_true_angles(d1, d2, baseline):

    # theta1 계산 (sin(t1) = (d1^2 + B^2 - d2^2) / (2 * d1 * B))
    sin_t1 = (d1**2 + baseline**2 - d2**2) / (2 * d1 * baseline)
    
    # theta2 계산 (sin(t2) = (d2^2 + B^2 - d1^2) / (2 * d2 * B))
    sin_t2 = (d2**2 + baseline**2 - d1**2) / (2 * d2 * baseline)
    
    # 예외 처리 (삼각형이 성립되지 않는 거리일 경우)
    if abs(sin_t1) > 1 or abs(sin_t2) > 1:
        raise ValueError("입력한 거리로는 삼각형을 만들 수 없습니다 (거리가 너무 짧거나 깁니다).")

    t1_rad = np.arcsin(sin_t1)
    t2_rad = np.arcsin(sin_t2)
    
    return t1_rad, t2_rad


def solve_general_triangulation():
    # ---------------------------------------------------------------------
    # 1. 고정 계수 (Calibration Coefficients)
    # ---------------------------------------------------------------------
    # [사진 속 수식] M = d*a1 + theta*a2 + a3
    a1 = 0.970188
    a2 = -0.177800
    a3 = 0.064273 

    # ---------------------------------------------------------------------
    # 2. 데이터 입력
    # ---------------------------------------------------------------------
    print("=== [데이터 입력] ===")
    
    # 측정값 (Measured Values)
    M1 = 1.78025  
    M2 = 1.91219 
    
    # 센서 간 거리 (Baseline)
    # 사진의 식: 1.75sin(t1) + 1.95sin(t2) = 2  ---> 즉, 전체 폭은 2m
    h = 2.0 

    # [검증용 참값]
    true_d1 = 1.75
    true_d2 = 1.95
    true_t1,true_t2 = calculate_true_angles(true_d1,true_d2,h)

    true_t1 = np.degrees(true_t1)
    true_t2 = np.degrees(true_t2)

    print(true_t1)
    print(true_t2)

if __name__ == "__main__":
    solve_general_triangulation()