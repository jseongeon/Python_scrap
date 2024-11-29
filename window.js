window.onload = function () {
    const handwrittenText = document.getElementById("handwrittenText");
    const underlineLine = document.querySelector(".underline-line");
    const text = handwrittenText.innerText;

    let index = 0;

    // 타이핑 애니메이션
    function typeText() {
        if (index < text.length) {
            handwrittenText.innerText = text.substring(0, index + 1);
            index++;
            setTimeout(typeText, 100); // 한 글자씩 100ms 간격으로 표시
        } else {
            // 밑줄 애니메이션 시작
            underlineLine.style.width = `${handwrittenText.clientWidth}px`;  // 밑줄 길이를 텍스트 길이에 맞추기
        }
    }

    typeText();
};
