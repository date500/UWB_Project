import numpy as np
from scipy.optimize import fsolve
import pandas as pd 

def calculate_true_angles(d1, d2, baseline):
    # 분모 0 방지 및 안전장치
    if d1 == 0 or d2 == 0 or baseline == 0:
        return np.nan, np.nan

    val1 = (d1**2 + baseline**2 - d2**2) / (2 * d1 * baseline)
    val2 = (d2**2 + baseline**2 - d1**2) / (2 * d2 * baseline)
    
    # 아크사인 범위 체크
    if abs(val1) > 1: val1 = np.nan
    if abs(val2) > 1: val2 = np.nan

    return np.arcsin(val1), np.arcsin(val2)

def solve_general_triangulation():
    # ---------------------------------------------------------
    # 1. 설정 및 데이터 로드
    # ---------------------------------------------------------
    file_path = '/home/user/jin/UWB_Project/srcs/Parameter/value/Case2.csv'
    
    # [경로 확인] 본인 윈도우 ID 확인 필수
    output_excel_path = '/mnt/c/Users/user/Desktop/새 폴더/Result_Case2.xlsx'
    
    try:
        data = np.loadtxt(file_path, delimiter=',')
        print(f"File Loaded: {file_path} ({len(data)} rows)")
    except Exception as e:
        print(f"File Load Error: {e}")
        return

    # Constants
    a1, a2, a3 = 0.970188, -0.177800, 0.064273 
    BASELINE = 3
    true_d1, true_d2 = 2.5, 2.1
    
    true_t1_rad, true_t2_rad = calculate_true_angles(true_d1, true_d2, BASELINE)
    true_t1_deg = np.degrees(true_t1_rad)
    true_t2_deg = np.degrees(true_t2_rad)

    # [추가됨] 참값 각도 정보 출력
    print(f"Ref True Values: d1={true_d1}, d2={true_d2}")
    print(f"Ref True Angles: t1={true_t1_deg:.4f}°, t2={true_t2_deg:.4f}°")

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
    print(f"{'Idx':<4} | {'d1':<9} {'d2':<9} | {'t1':<9} {'t2':<9} || {'Err_d1':<9} {'Err_d2':<9} | {'Err_t1':<9} {'Err_t2':<9}")
    print("="*120)

    excel_data = [] 
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
        
        # [수정됨] 절대값(abs) 제거 -> 단순 오차 (측정값 - 참값)
        e_d1 = c_d1 - true_d1
        e_d2 = c_d2 - true_d2
        e_t1 = c_t1_deg - true_t1_deg
        e_t2 = c_t2_deg - true_t2_deg
        
        # 화면 출력 (Console)
        print(f"{i:<4} | {c_d1:<9.5f} {c_d2:<9.5f} | {c_t1_deg:<9.4f} {c_t2_deg:<9.4f} || {e_d1:<9.5f} {e_d2:<9.5f} | {e_t1:<9.4f} {e_t2:<9.4f}")

        # 엑셀 데이터 저장
        excel_data.append({
            'IDX': i,
            'M1': m1_in,
            'M2': m2_in,
            'd1': c_d1,
            'd2': c_d2,
            't1(deg)': c_t1_deg,
            't2(deg)': c_t2_deg,
            'Err_d1': e_d1,
            'Err_d2': e_d2,
            'Err_t1': e_t1,
            'Err_t2': e_t2
        })
        last_sol = sol

    # ---------------------------------------------------------
    # 3. 엑셀 저장
    # ---------------------------------------------------------
    df = pd.DataFrame(excel_data)
    
    avg_row = df.mean(numeric_only=True).astype(object)
    avg_row['IDX'] = 'AVG' 
    
    df_final = pd.concat([df, pd.DataFrame([avg_row])], ignore_index=True)

    df_final = df_final.round(4)
    
    df_final = df_final.replace([np.inf, -np.inf], np.nan)
    df_final = df_final.fillna('')

    try:
        df_final.to_excel(output_excel_path, index=False, engine='openpyxl')
        print("\n" + "="*60)
        print(f"✅ Excel Saved! Path: {output_excel_path}")
        print("="*60)
    except Exception as e:
        print(f"\n❌ Save Failed: {e}")

    print("\n=== [Final Averages] ===")
    print(f" Avg d1: {avg_row['d1']:.5f} m")
    print(f" Avg d2: {avg_row['d2']:.5f} m")

if __name__ == "__main__":
    solve_general_triangulation()