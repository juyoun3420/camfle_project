var star = 0;
var current = 0;

document.getElementById("current").innerHTML = current;

function updateChargeAmount(amount) {
    star = star + amount;
    document.getElementById("chargeAmount").innerHTML = star;
}

function click_starBtn() {
    alert(star + " 스타 충전 완료!");
    current = current + star;
    document.getElementById("current").innerHTML = current;

    // 입력 필드 초기화
    const chargeAmountInput = document.getElementById("chargeAmount");
    chargeAmountInput.value = ""; // 입력 필드를 빈 문자열로 설정하여 초기화
}

const btn1 = document.getElementById("btn1");
btn1.addEventListener("click", function () {
    updateChargeAmount(1000);
});

const btn2 = document.getElementById("btn2");
btn2.addEventListener("click", function () {
    updateChargeAmount(2000);
});

const btn3 = document.getElementById("btn3");
btn3.addEventListener("click", function () {
    updateChargeAmount(5000);
});

const btn4 = document.getElementById("btn4");
btn4.addEventListener("click", function () {
    updateChargeAmount(10000);
});

const btn5 = document.getElementById("btn5");
btn5.addEventListener("click", function () {
    updateChargeAmount(20000);
});

const btn6 = document.getElementById("btn6");
btn6.addEventListener("click", function () {
    updateChargeAmount(30000);
});

const starButton = document.getElementById("starBtn");
starButton.addEventListener("click", click_starBtn);

// 초기화 버튼 처리
const resetButton = document.querySelector('input[type="reset"]');
resetButton.addEventListener('click', function () {
    star = 0;
    document.getElementById("chargeAmount").innerHTML = star;
});

// 스타 잔액 업데이트
const starBalanceElement = document.getElementById("star_balance");
starBalanceElement.textContent = current; // current 값을 star_balance에 복사

// 스타 잔액 정보를 로컬 스토리지에 저장
function updateStarBalance(current) {
    localStorage.setItem('starBalance', current);
}

// 스타 잔액 정보를 가져와 출력
function displayStarBalance() {
    const starBalanceElement = document.getElementById('star_balance');
    const starBalance = localStorage.getItem('starBalance') || '0'; // 기본값은 0
    starBalanceElement.textContent = starBalance;
}