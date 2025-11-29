1. 데이터 로드 및 병합:
- spaceship-titanic 디렉토리의 train.csv, test.csv, sample_submission.csv 파일을 읽어왔습니다.
- test.csv에는 Transported 정보가 없으므로, sample_submission.csv의 내용을 PassengerId 기준으로 병합하여 Transported 값을 채웠습니다.
- 그 후 train.csv와 병합된 test 데이터를 하나로 합쳤습니다.

2. 전체 데이터 수량 파악:
- 병합된 전체 데이터의 개수는 12,970개입니다.

3. 상관관계 분석:
- Transported 항목과 가장 관련성이 높은(상관계수가 가장 큰) 항목을 분석했습니다.
- 분석 결과, CryoSleep (동면 여부) 항목이 가장 높은 상관관계를 보였습니다. (상관계수: 약 0.3258)

4. 연령대별 그래프 출력:
- 나이(Age)를 기준으로 10대부터 70대까지 그룹화했습니다.
- 각 연령대별로 Transported 여부(True/False)의 분포를 보여주는 그래프를 생성하여 age_transported_graph.png 파일로 저장했습니다.