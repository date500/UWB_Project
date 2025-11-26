import numpy as np
from scipy.optimize import fsolve # 방정식을 풀기 위한 도구

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
    BASELINE = 2.0 

    # [검증용 참값]
    true_d1 = 1.75
    true_theta1_deg = 27.756459
    true_d2 = 1.95
    true_theta2_deg = 37.422828

    print(f" 측정값 1 (M1) : {M1}")
    print(f" 측정값 2 (M2) : {M2}")
    print(f" 센서 간격 (2h) : {BASELINE} m")
    print("-" * 40)

    # ---------------------------------------------------------------------
    # 3. 알고리즘: 연립 방정식 정의
    # ---------------------------------------------------------------------
    # 우리가 구해야 할 미지수: d1, theta1, d2, theta2 (총 4개)
    # 입력 변수 x = [d1, theta1, d2, theta2]
    
    def equations(vars):
        d1, t1, d2, t2 = vars # t1, t2는 라디안 단위
        
        # 식 1: 센서 1 모델 (M1 = d1*a1 + t1*a2 + a3)
        eq1 = (d1 * a1) + (t1 * a2) + a3 - M1
        
        # 식 2: 센서 2 모델 (M2 = d2*a1 + t2*a2 + a3)
        eq2 = (d2 * a1) + (t2 * a2) + a3 - M2
        
        # 식 3: 기하학적 조건 X축 (d1*cos(t1) = d2*cos(t2))
        eq3 = d1 * np.cos(t1) - d2 * np.cos(t2)
        
        # 식 4: 기하학적 조건 Y축 (d1*sin(t1) + d2*sin(t2) = 2)
        eq4 = d1 * np.sin(t1) + d2 * np.sin(t2) - BASELINE
        
        return [eq1, eq2, eq3, eq4]

    # ---------------------------------------------------------------------
    # 4. 방정식 풀이 (Solver 실행)
    # ---------------------------------------------------------------------
    # 초기 추정값 (Initial Guess) - 해를 잘 찾기 위해 대략적인 값을 넣어줍니다.
    # 거리값은 M값과 비슷할 것이고, 각도는 0.5 라디안 정도로 가정
    initial_guess = [1.8, 0.5, 1.9, 0.6] 
    
    # fsolve로 4개의 미지수를 한 번에 계산
    solution = fsolve(equations, initial_guess)
    
    calc_d1, calc_t1_rad, calc_d2, calc_t2_rad = solution
    
    # 라디안 -> 도(degree) 변환
    calc_t1_deg = np.degrees(calc_t1_rad)
    calc_t2_deg = np.degrees(calc_t2_rad)

    # ---------------------------------------------------------------------
    # 5. 결과 출력 및 오차 검증
    # ---------------------------------------------------------------------
    print("\n=== [분석 결과 (사진 알고리즘 적용)] ===")
    print(f" [센서 1] 추정 거리: {calc_d1:.5f} m | 추정 각도: {calc_t1_deg:.5f} 도 ({calc_t1_rad:.5f} rad)")
    print(f" [센서 2] 추정 거리: {calc_d2:.5f} m | 추정 각도: {calc_t2_deg:.5f} 도 ({calc_t2_rad:.5f} rad)")

    print("\n=== [오차 검증] ===")
    # 오차 1 (센서 1)
    err_d1 = abs(calc_d1 - true_d1)
    err_t1 = abs(calc_t1_deg - true_theta1_deg)
    print(f" [Set 1] 거리오차: {err_d1:.6f} m | 각도오차: {err_t1:.6f} 도")

    # 오차 2 (센서 2)
    err_d2 = abs(calc_d2 - true_d2)
    err_t2 = abs(calc_t2_deg - true_theta2_deg)
    print(f" [Set 2] 거리오차: {err_d2:.6f} m | 각도오차: {err_t2:.6f} 도")

    # 정확도 (거리 기준)
    print("-" * 40)
    print(f" * Set 1 거리 정확도: {100 - (err_d1/true_d1*100):.4f}%")
    print(f" * Set 2 거리 정확도: {100 - (err_d2/true_d2*100):.4f}%")

if __name__ == "__main__":
    solve_general_triangulation()