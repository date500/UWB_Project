# 📡 UWB Sensor Calibration & Distance Estimation
> UWB 센서의 측정 정밀도 향상을 위한 데이터 분석 및 파라미터 보정 프로젝트

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📖 프로젝트 개요 (Overview)
이 프로젝트는 UWB(Ultra-Wideband) 센서를 활용하여 물체의 위치를 측정할 때 발생하는 **거리 및 각도에 따른 오차를 보정**하기 위해 진행되었습니다.
실제 거리와 각도에 따라 수집된 센서 데이터를 분석하고, **최소자승법(Least Squares Method)**을 적용하여 최적의 보정 계수($a_1, a_2, a_3$)를 도출하는 것을 목표로 합니다.

## 🎯 핵심 목표 (Objectives)
* 다양한 거리(1m~3m)와 각도(0°~30°) 환경에서 UWB 센서 데이터 수집
* 수집된 데이터를 분석하기 쉬운 형태(CSV)로 전처리
* **다중 선형 회귀(Multiple Linear Regression)** 모델을 통한 보정 공식 도출
* 측정 오차를 최소화하는 파라미터 $a_1, a_2, a_3$ 산출

## 🛠️ 기술 스택 (Tech Stack)
* **Language:** Python 3.x
* **Libraries:**
    * `pandas`: 대용량 센서 데이터 로딩 및 전처리 (Wide to Long format 변환)
    * `scikit-learn`: 선형 회귀 모델 학습 및 계수 추출
    * `numpy`: 수치 계산 및 라디안(Radian) 변환

## 📊 수학적 모델 (Mathematical Model)
센서의 측정값($Y$)은 실제 거리($X_{dist}$)와 각도($X_{angle}$)에 선형적으로 비례한다고 가정하고, 아래와 같은 보정 공식을 수립했습니다.
정확한 계산을 위해 각도(Degree)는 **라디안(Radian)**으로 변환하여 적용했습니다.

$$\text{Measured Value} = \text{Real Dist} \cdot a_1 + \text{Angle(rad)} \cdot a_2 + a_3$$

* **$a_1$**: 거리 가중치 (Distance Coefficient)
* **$a_2$**: 각도 가중치 (Angle Coefficient)
* **$a_3$**: 기본 오차 상수 (Intercept)

## 📂 프로젝트 구조 (Project Structure)
```bash
├── data/
│   ├── 1m_parameter.csv    # 원본 센서 데이터 (Raw Data)
│   └── final_data.csv      # 전처리 완료된 데이터 (Processed Data)
├── src/
│   ├── data_converter.py   # 데이터 포맷 변환 스크립트
│   └── parameter_calc.py   # 회귀분석 및 계수 산출 스크립트
├── requirements.txt        # 필요 라이브러리 목록
└── README.md