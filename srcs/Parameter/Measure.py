import numpy as np
from scipy.optimize import fsolve
import csv  # 파이썬 기본 내장 (설치 불필요)

def calculate_true_angles(d1, d2, baseline):
    sin_t1 = (d1**2 + baseline**2 - d2**2) / (2 * d1 * baseline)
    sin_t2 = (d2**2 + baseline**2 - d1**2) / (2 * d2 * baseline)
    
    if abs(sin_t1) > 1 or abs(sin_t2) > 1:
        raise ValueError("삼각형 성립 조건 위배.")

    return np.arcsin(sin_t1), np.arcsin(sin_t2)

def solve_general_triangulation():
    # ---------------------------------------------------------
    # 1. 설정 및 데이터 로드
    # ---------------------------------------------------------
    file_path = '/home/user/jin/UWB_Project/srcs/Parameter/value/Case3.csv'
    # 저장할 경로 (.csv로 변경)
    output_csv_path = '/home/user/jin/UWB_Project/srcs/Parameter/value/Result_Case3.csv'
    
    try:
        data = np.loadtxt(file_path, delimiter=',')
        print(f"파일 로드 완료: {file_path} (데이터 {len(data)}개)")
    except Exception as e:
        print(f"파일 로드 실패: {e}")
        return

    # 파라미터
    a1, a2, a3 = 0.970188, -0.177800, 0.064273 
    BASELINE = 2.0 
    true_d1, true_d2 = 1.75, 1.95
    
    true_t1_rad, true_t2_rad = calculate_true_angles(true_d1, true_d2, BASELINE)
    true_t1_deg = np.degrees(true_t1_rad)
    true_t2_deg = np.degrees(true_t2_rad)

    print(f"참값 기준: d1={true_d1}, d2={true_d2}")

    def equations(vars, m1, m2):
        d1, t1, d2, t2 = vars
        eq1 = (d1 * a1) + (t1 * a2) + a3 - m1
        eq2 = (d2 * a1) + (t2 * a2) + a3 - m2
        eq3 = d1 * np.cos(t1) - d2 * np.cos(t2)
        eq4 = d1 * np.sin(t1) + d2 * np.sin(t2) - BASELINE
        return [eq1, eq2, eq3, eq4]

    # ---------------------------------------------------------
    # 2. 데이터 처리
    # ---------------------------------------------------------
    print("="*120)
    print(f"{'순번':<4} | {'추정_d1':<9} {'추정_d2':<9} | {'추정_t1':<9} {'추정_t2':<9} || {'오차_d1':<9} {'오차_d2':<9} | {'오차_t1':<9} {'오차_t2':<9}")
    print("="*120)

    # CSV 헤더 정의
    csv_header = ['순번', '입력_M1', '입력_M2', '추정_d1', '추정_d2', '추정_t1', '추정_t2', '오차_d1', '오차_d2', '오차_t1', '오차_t2']
    csv_rows = [] # 데이터를 모을 리스트
    
    last_sol = None

    for i, row in enumerate(data):
        m1_in, m2_in = row[0], row[1]
        
        if last_sol is None:
            guess = [m1_in, 0.5, m2_in, 0.5] 
        else:
            guess = last_sol 
        
        sol = fsolve(equations, guess, args=(m1_in, m2_in))
        c_d1, c_t1_rad, c_d2, c_t2_rad = sol
        
        c_t1_deg = np.degrees(c_t1_rad)
        c_t2_deg = np.degrees(c_t2_rad)
        
        e_d1 = abs(c_d1 - true_d1)
        e_d2 = abs(c_d2 - true_d2)
        e_t1 = abs(c_t1_deg - true_t1_deg)
        e_t2 = abs(c_t2_deg - true_t2_deg)
        
        # 화면 출력
        print(f"{i:<4} | {c_d1:<9.5f} {c_d2:<9.5f} | {c_t1_deg:<9.4f} {c_t2_deg:<9.4f} || {e_d1:<9.5f} {e_d2:<9.5f} | {e_t1:<9.4f} {e_t2:<9.4f}")

        # 리스트에 저장 (모든 수치는 소수점 6자리까지 저장 권장)
        csv_rows.append([
            i, m1_in, m2_in, 
            c_d1, c_d2, c_t1_deg, c_t2_deg, 
            e_d1, e_d2, e_t1, e_t2
        ])

        last_sol = sol

    # ---------------------------------------------------------
    # 3. 평균 계산 및 CSV 저장
    # ---------------------------------------------------------
    # numpy를 이용해 열별 평균 계산 (순번 제외)
    data_matrix = np.array([row[1:] for row in csv_rows]) # 0번째 열(순번) 뺌
    averages = np.mean(data_matrix, axis=0)
    
    # 평균 행 생성 ('순번' 자리에 '평균' 텍스트 넣기)
    avg_row = ['평균'] + averages.tolist()

    # CSV 파일 쓰기
    try:
        # utf-8-sig는 엑셀에서 한글 깨짐 방지용 인코딩입니다.
        with open(output_csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)   # 헤더 쓰기
            writer.writerows(csv_rows)    # 데이터 쓰기
            writer.writerow(avg_row)      # 평균 쓰기
            
        print("\n" + "="*60)
        print(f"✅ CSV 파일 저장 성공! 경로: {output_csv_path}")
        print("="*60)
    except Exception as e:
        print(f"\n❌ CSV 저장 실패: {e}")

    # 화면에 평균 요약 출력
    print("\n=== [최종 평균] ===")
    print(f" 평균 d1: {averages[2]:.5f} m") # index 2가 d1 (M1, M2 다음)
    print(f" 평균 d2: {averages[3]:.5f} m")

if __name__ == "__main__":
    solve_general_triangulation()