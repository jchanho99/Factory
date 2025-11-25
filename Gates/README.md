## 해당 디렉토리 목표
- 공장 출입구 디지털화

## 작동 방법
1. 차량 번호를 확인해 DB와 비교
2. 사무실 출입구에서 사원 인증
3. (1)과 (2) 방식 성공 시 공장 설비 출입구 개방

## 구현 방법
### 사용 언어
- Python (version: `3.14.0`)
### 인프라 적용 정보
- Docker를 이용한 컨테이너화
- 개방 포트번호: `8000`
### 디렉토리 별 사용 라이브러리 정리
#### Plate
- 번호판 인식 데이터: [AIHUB](https://aihub.or.kr/aihubdata/data/view.do?srchOptnCnd=OPTNCND001&currMenu=115&topMenu=100&searchKeyword=%EB%B2%88%ED%98%B8%ED%8C%90&aihubDataSe=data&dataSetSn=172)
#### MainGate
#### EquimentGate