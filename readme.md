
[ CAMFLE Introducing ]

접속 url : https://givoandtake.run.goorm.io/list
* 접속 계정은
  ID : hyemin / PW : hyemin 사용 *


* 파일 구조<br>
camfle_project/<br>
├── .gitignore<br>
├── LICENSE<br>
├── application.py<br>
├── database.py<br>
├── goorm.manifest<br>
├── readme.md<br>
├── authentication/<br>
│   ├── __init__.py<br>
│   ├── auth_routes.py<br>
│   └── ...<br>
├── static/<br>
│   ├── css/<br>
│   │   └── styles.css<br>
│   ├── js/<br>
│   │   └── scripts.js<br>
│   └── ...<br>
└── templates/<br>
    ├── detail.html<br>
    ├── index.html<br>
    ├── list.html<br>
    ├── login.html<br>
    ├── mypage_like.html<br>
    ├── mypage_review.html<br>
    ├── mypage_sell.html<br>
    ├── reg_items.html<br>
    ├── reg_reviews.html<br>
    ├── review.html<br>
    ├── review_detail.html<br>
    ├── signup.html<br>
    ├── submit_item_result.html<br>
    ├── timetable_match.html<br>
    └── ...<br>

* 주요 코드 설명
   1. 물품 적정 가격 추천
      ![상품 등록 화면](https://github.com/juyoun3420/camfle_project/blob/week11-2/1.%20%EC%82%AC%EC%A7%84.png)
      - 사용자가 중고 물품을 등록할 때 물품의 카테고리, 구매시기, 사용횟수 등의 정보를 입력하면 자체 알고리즘을 통해 적정 가격을 계산하여 추천합니다.
      - 사용자는 추천 가격을 그대로 사용하거나, 본인이 선택한 가격을 사용할 수 있습니다.
      - 물품 리스트 창에서 추천 가격 대비 현재 가격의 적정 여부를 쉽게 파악할 수 있습니다.
   2. 시간표 매칭 서비스
      ![시간표 매칭 화면1](https://github.com/juyoun3420/camfle_project/blob/week11-2/2-1.%EC%82%AC%EC%A7%84.png)

      ![시간표 매칭 화면2](https://github.com/juyoun3420/camfle_project/blob/week11-2/2-2.%EC%82%AC%EC%A7%84.png)
      - 사용자가 구매 버튼을 누르면 현재 등록된 다른 사용자들의 시간표와 비교하여 일치하는 공강 시간을 최대 3개까지 추천합니다.
      - 실제 이화여대 시간표와 유사한 구조로 9시부터 6시까지 1시간 15분 수업, 15분 공강 시간으로 구성되어 있습니다.
      - 사용자의 매칭 화면은 네비게이터 바를 통해 "{{id}}님 반갑습니다!" 메뉴로 연결됩니다.
* HOW TO BUILD
  - Python 3.x 설치
  - Flask 프레임워크 설치
  - SQLite 데이터베이스 설치
  - 의존성 패키지 설치 : `pip install -r requirements.txt`

* HOW TO INSTALL
  - 레포지토리 클론 : `git clone https://github.com/your-username/camfle-project.git`
  - 가상환경 생성 및 활성화
  - 의존성 패키지 설치 : `pip install -r requirements.txt`
  - 데이터베이스 초기화 : `python database.py`
  - 서버 실행 : `python application.py`

* HOW TO TEST
  - 웹 브라우저에서 `http://localhost:5000/list` 접속
  - 회원가입 및 로그인 테스트
  - 물품 등록 및 구매 테스트
  - 시간표 매칭 기능 테스트
  - 리뷰 작성 및 조회 테스트       


      
