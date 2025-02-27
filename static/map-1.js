document.addEventListener("DOMContentLoaded", function () {
    // Инициализация карты с центром в Казахстане
    var map = L.map('map').setView([48.0196, 66.9237], 5);
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
                let marker = L.marker([item.lat, item.lng], { title: "Fire Score: " + item.fire_score });
                marker.bindPopup(`<strong>Fire Score: ${item.fire_score}</strong>`);
                markersLayer.addLayer(marker);

                // Определяем стиль для круга (полигона) в зависимости от fire_score
                let color = 'green';
                if (item.fire_score === "в процессе проверки") {
                    color = 'gray';
                } else {
                    let score = parseFloat(item.fire_score);
                    if (!isNaN(score)) {
                        if (score >= 7.0) {
                            color = 'red';
                        } else if (score >= 4.0) {
                            color = 'orange';
                        } else {
                            color = 'green';
                        }
                    } else {
                        color = 'gray';
                    }
                }

                // Создаем круг с фиксированным радиусом (например, 5000 метров)
                let circle = L.circle([item.lat, item.lng], {
                    radius: 5000,
                    color: color,
                    fillOpacity: 0.5
                });
                circle.bindPopup(`<strong>Fire Score: ${item.fire_score}</strong>`);
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
            // Режим маркеров: удаляем riskLayer и добавляем markersLayer
            if (map.hasLayer(riskLayer)) {
                map.removeLayer(riskLayer);
            }
            map.addLayer(markersLayer);
        } else {
            // Режим разукрашенной карты: удаляем markersLayer и добавляем riskLayer
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
                // Закрываем все открытые ответы
                document.querySelectorAll(".faq-answer").forEach(a => a.classList.remove("active"));
                document.querySelectorAll(".faq-toggle").forEach(t => t.textContent = "+");
                answer.classList.add("active");
                toggle.textContent = "−";
            }
        });
    });
});
