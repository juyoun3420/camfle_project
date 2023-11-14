// 사용자 프로필 이미지와 키워드 목록 요소 가져오기
const userProfileImage = document.getElementById('user-profile-image');
const userImagePaths = [
    '사용자1의 프로필 이미지 경로',
    '사용자2의 프로필 이미지 경로',
    // 여러 사용자의 이미지 경로를 추가합니다.
];

// keywordList 요소 가져오기
const keywordList = document.getElementById("keywordList");

// keywordForm 요소 가져오기
const keywordForm = document.getElementById("keywordForm");

// 입력 필드 초기화
const keywordInput = document.getElementById("keyword");

// 키워드 입력 폼 제출 이벤트 처리
keywordForm.addEventListener("submit", function (event) {
    event.preventDefault(); // 폼 제출 기본 동작 방지

    // 입력된 키워드 가져오기
    const keyword = keywordInput.value;

    // 현재 키워드 목록 가져오기
    const keywords = keywordList.querySelectorAll("li");

    // 목록에 추가된 키워드가 4개 미만인 경우에만 추가
    if (keywords.length < 4) {
        // 새로운 키워드를 목록에 추가
        const listItem = document.createElement("li");
        listItem.textContent = keyword;

        // 삭제 버튼 추가
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "X";
        deleteButton.className = "delete-button";

        deleteButton.addEventListener("click", function () {
            // 삭제 버튼을 클릭할 때 해당 항목을 삭제합니다.
            listItem.remove();
        });

        listItem.appendChild(deleteButton);

        keywordList.appendChild(listItem);

        // 입력 필드 초기화
        keywordInput.value = "";
    }
    // 가상의 데이터 (date와 stardonation에 대한 데이터)
    const data = {
        labels: ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"],
        datasets: [
            {
                label: "스타 기부",
                data: [1000, 2000, 1500, 2500, 1800],
                borderColor: "#F44D99",
                backgroundColor: "transparent",
            },
        ],
    };

    // 그래프를 그릴 canvas 요소 가져오기
    const ctx = document.getElementById("myChart").getContext("2d");

    // 차트 데이터 예시 (날짜와 스타 기부량)
    const dates = ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'];
    const starDonations = [100, 250, 150, 300, 200];

    // 그래프 생성
    const ctx = document.getElementById('myChart').getContext('2d');

    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates, // x축 레이블 (날짜)
            datasets: [{
                label: '스타 기부량',
                data: starDonations, // y축 데이터 (스타 기부량)
                borderColor: 'rgb(255, 99, 132)',
                borderWidth: 2,
                fill: false, // 선 그래프로 만들기
            }],
        },
        options: {
            scales: {
                x: [{
                    display: true,
                }],
                y: [{
                    display: true,
                    beginAtZero: true,
                }],
            },
        },
    })
};