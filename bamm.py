import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

def draw_sensor_geometry():
    # 1. 설정값 정의
    d1 = 1.9
    d2 = 2.25
    theta1_deg = 26.04
    theta2_deg = 40.65
    baseline = 2.3
    
    # 각도를 라디안으로 변환
    theta1_rad = np.radians(theta1_deg)
    theta2_rad = np.radians(theta2_deg)
    
    # 2. 좌표 계산
    # 센서 2를 원점(0,0)으로, 센서 1을 (0, 2)로 설정 (수직 배치)
    sensor2_pos = np.array([0, 0])
    sensor1_pos = np.array([0, baseline])
    
    # 물체(Target)의 위치 계산
    # 기하학적 조건: x = d * cos(theta), y_offset = d * sin(theta)
    # 센서 2 기준으로 계산:
    target_x = d2 * np.cos(theta2_rad)
    target_y = d2 * np.sin(theta2_rad)
    target_pos = np.array([target_x, target_y])
    
    # 검증: 센서 1 기준 위치와 일치하는지 확인
    # 센서 1에서 물체까지의 y거리 = 2.0 - target_y
    # 계산된 y거리 = d1 * sin(theta1)
    check_y_gap = baseline - target_y
    calc_y_gap = d1 * np.sin(theta1_rad)
    
    print(f"좌표 검증:")
    print(f"Target 위치: ({target_x:.3f}, {target_y:.3f})")
    print(f"센서1-물체 수직거리(기하학): {check_y_gap:.3f}")
    print(f"센서1-물체 수직거리(수식): {calc_y_gap:.3f}")

    # 3. 그래프 그리기
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 센서 및 물체 점 찍기
    ax.scatter(*sensor1_pos, color='blue', s=100, label='Sensor 1', zorder=5)
    ax.scatter(*sensor2_pos, color='green', s=100, label='Sensor 2', zorder=5)
    ax.scatter(*target_pos, color='red', s=150, marker='*', label='Object (Target)', zorder=5)
    
    # 선 그리기 (센서-물체, 센서간 베이스라인)
    ax.plot([sensor1_pos[0], target_pos[0]], [sensor1_pos[1], target_pos[1]], 'b--', alpha=0.6)
    ax.plot([sensor2_pos[0], target_pos[0]], [sensor2_pos[1], target_pos[1]], 'g--', alpha=0.6)
    ax.plot([sensor1_pos[0], sensor2_pos[0]], [sensor1_pos[1], sensor2_pos[1]], 'k-', linewidth=3, alpha=0.3, label='Baseline (2m)')

    # 기준선 (각도 표시용 수평선)
    # 센서 1 기준선
    ax.plot([sensor1_pos[0], sensor1_pos[0]+0.5], [sensor1_pos[1], sensor1_pos[1]], 'k:', alpha=0.5)
    # 센서 2 기준선
    ax.plot([sensor2_pos[0], sensor2_pos[0]+0.5], [sensor2_pos[1], sensor2_pos[1]], 'k:', alpha=0.5)

    # 4. 텍스트 및 주석 추가
    # 센서 이름
    ax.text(sensor1_pos[0]-0.1, sensor1_pos[1], 'Sensor 1', ha='right', va='center', fontweight='bold')
    ax.text(sensor2_pos[0]-0.1, sensor2_pos[1], 'Sensor 2', ha='right', va='center', fontweight='bold')
    ax.text(target_pos[0]+0.1, target_pos[1], 'Object', ha='left', va='center', fontweight='bold', color='red')
    
    # 거리 텍스트
    ax.text(target_pos[0]/2, (sensor1_pos[1] + target_pos[1])/2 + 0.1, f'd1 = {d1}m', color='blue', fontsize=10)
    ax.text(target_pos[0]/2, (sensor2_pos[1] + target_pos[1])/2 - 0.1, f'd2 = {d2}m', color='green', fontsize=10)
    ax.text(-0.15, baseline/2, f'{baseline}m', ha='right', va='center', fontsize=12)

    # 각도 호(Arc) 그리기
    # Sensor 1 Angle (아래쪽 방향)
    arc1 = patches.Arc(sensor1_pos, 1.0, 1.0, theta1=0.0, theta2=0.0, angle=-theta1_deg, color='blue') 
    # 주의: Arc 그리는 방식이 복잡할 수 있어 텍스트로 대체하거나 간단히 표현
    
    # 각도 텍스트
    ax.text(0.4, sensor1_pos[1] - 0.1, f'{theta1_deg}°', color='blue', fontsize=9)
    ax.text(0.4, sensor2_pos[1] + 0.1, f'{theta2_deg}°', color='green', fontsize=9)

    # 설정
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_title("Dual UWB Sensor Geometry", fontsize=14)
    ax.set_xlabel("Horizontal Distance (m)")
    ax.set_ylabel("Vertical Distance (m)")
    ax.set_xlim(-0.5, 3.0)
    ax.set_ylim(-0.5, 3.0)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_sensor_geometry()