document.addEventListener("DOMContentLoaded", function () {
    // Инициализируем карту
    var map = L.map('map').setView([49.0196, 62.9237], 5); // Центр Казахстана

    // Добавляем слой 2ГИС (используем API токен)
    L.tileLayer(`https://tile2.maps.2gis.com/tiles?x={x}&y={y}&z={z}&key=26a4d1c1-3965-4dcd-977e-e01e116fed8f`, {
        attribution: '&copy; 2ГИС'
    }).addTo(map);
});

document.addEventListener("DOMContentLoaded", function () {
    // Инициализируем карту
    var map = L.map('map').setView([48.0196, 66.9237], 5); // Центр Казахстана

    // Добавляем слой 2ГИС (используем API токен)
    L.tileLayer(`https://tile2.maps.2gis.com/tiles?x={x}&y={y}&z={z}&key=26a4d1c1-3965-4dcd-977e-e01e116fed8f`, {
        attribution: '&copy; 2ГИС'
    }).addTo(map);

    // Открытие/закрытие FAQ вопросов
    document.querySelectorAll(".faq-question").forEach(button => {
        button.addEventListener("click", function () {
            let answer = this.nextElementSibling;
            answer.style.display = answer.style.display === "block" ? "none" : "block";
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const questions = document.querySelectorAll(".faq-question");

    questions.forEach(question => {
        question.addEventListener("click", function () {
            let answer = this.nextElementSibling;
            let toggle = this.querySelector(".faq-toggle");

            if (answer.classList.contains("active")) {
                answer.classList.remove("active");
                toggle.textContent = "+";
            } else {
                document.querySelectorAll(".faq-answer").forEach(a => a.classList.remove("active"));
                document.querySelectorAll(".faq-toggle").forEach(t => t.textContent = "+");

                answer.classList.add("active");
                toggle.textContent = "−";
            }
        });
    });
});
