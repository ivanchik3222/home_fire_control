document.addEventListener("DOMContentLoaded", function () {
    // Инициализация карты с центром в Казахстане
    var map = L.map('map').setView([54.9833, 69.3833], 12);  // Центр Петропавловска, увеличил масштаб

    L.tileLayer(`https://tile2.maps.2gis.com/tiles?x={x}&y={y}&z={z}&key=26a4d1c1-3965-4dcd-977e-e01e116fed8f`, {
        attribution: '&copy; 2ГИС'
    }).addTo(map);

    // Создаем два слоя: для маркеров и для рисковой карты (кругов)
    var markersLayer = L.layerGroup();
    var riskLayer = L.layerGroup();

    // Получаем данные из одного запроса
    fetch('/analytics/map_data')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                // Создаем маркер для каждого объекта
                let marker = L.marker([item.lat, item.lng], { title: "Уровень риска: " + item.fire_risk_level });
                marker.bindPopup(`<strong>Уровень риска: ${item.fire_risk_level}</strong>`);
                markersLayer.addLayer(marker);

                // Определяем цвет круга в зависимости от fire_risk_level
                let color;
                switch (item.fire_risk_level) {
                    case "пожаробезопасно":
                        color = "green";
                        break;
                    case "средней_опасности":
                        color = "orange";
                        break;
                    case "пожароопасно":
                        color = "red";
                        break;
                    default:
                        color = "gray";  // Если "в процессе проверки" или неизвестное значение
                }

                // Создаем круг с уменьшенным радиусом (2000 метров)
                let circle = L.circle([item.lat, item.lng], {
                    radius: 200,
                    color: color,
                    fillOpacity: 0.5
                });
                circle.bindPopup(`<strong>Уровень риска: ${item.fire_risk_level}</strong>`);
                riskLayer.addLayer(circle);
            });

            // Отображаем слой в зависимости от состояния переключателя
            var filterSwitch = document.getElementById("filter-switch");
            if (filterSwitch.checked) {
                map.addLayer(markersLayer);
            } else {
                map.addLayer(riskLayer);
            }
        })
        .catch(err => console.error('Ошибка получения данных:', err));

    // Обработчик переключения режимов отображения
    var filterSwitch = document.getElementById("filter-switch");
    filterSwitch.addEventListener("change", function () {
        if (this.checked) {
            if (map.hasLayer(riskLayer)) {
                map.removeLayer(riskLayer);
            }
            map.addLayer(markersLayer);
        } else {
            if (map.hasLayer(markersLayer)) {
                map.removeLayer(markersLayer);
            }
            map.addLayer(riskLayer);
        }
    });

    // Логика для FAQ вопросов (без изменений)
    document.querySelectorAll(".faq-question").forEach(button => {
        button.addEventListener("click", function () {
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
