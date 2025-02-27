ymaps.ready(init);
let objectsData = [];

async function init() {
    var myMap = new ymaps.Map("map", {
        center: [54.872013, 69.170711],
        zoom: 13,
        controls: []
    });

    try {
        let pointA = await getUserLocation();
        let pointB = getPoint(document.getElementById("coordinates").innerHTML);

        console.log("Координаты объекта:", document.getElementById("coordinates").innerHTML);

        console.log("Координаты пользователя:", pointA);

        var userPlacemark = new ymaps.Placemark(pointA, {
            balloonContent: "Вы здесь"
        }, {
            preset: "islands#blueDotIcon"
        });

        myMap.geoObjects.add(userPlacemark);
        myMap.setCenter(pointA, 14); // Центрируем карту на пользователе

        // Построение маршрута после получения координат
        ymaps.route([pointA, pointB]).then(
            function (route) {
                myMap.geoObjects.add(route);
            },
            function (error) {
                console.error("Ошибка построения маршрута: ", error);
            }
        );

    } catch (error) {
        console.error("Ошибка получения геолокации:", error);
    }
}

// Функция для получения координат пользователя
function getUserLocation() {
    return new Promise((resolve, reject) => {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(
                position => {
                    resolve([position.coords.latitude, position.coords.longitude]);
                },
                error => {
                    reject(error);
                }
            );
        } else {
            reject("Геолокация не поддерживается браузером");
        }
    });



}

function getPoint(str) {
    return str.split(",").map(Number);
}