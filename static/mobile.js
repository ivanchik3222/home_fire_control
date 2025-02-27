ymaps.ready(init);
let objectsData = [];

async function init() {
    var myMap = new ymaps.Map("map", {
        center: [54.872013, 69.170711],
        zoom: 13,
        controls: []
    });

    await loadObjects();

    for (let i = 0; i < objectsData.length; i++) {
        let coordinates = objectsData[i].coordinates;
        if (coordinates.includes(", ")) {
            coordinates = objectsData[i].coordinates.split(", ");
        } else {
            coordinates = objectsData[i].coordinates.split(" ");
        }

        var myGeoObject = new ymaps.Placemark([Number(coordinates[0]), Number(coordinates[1])], {
            balloonContentHeader: 'Однажды',
            balloonContentBody: '<button class="check-btn" data-index="' +  objectsData[i].object_id + '">Начать проверку</button>',
        }, {
            iconLayout: 'default#image',
            iconImageHref: '../static/materials/location.svg',
            iconImageSize: [30, 42],
            iconImageOffset: [-3, -42]
        });

        myMap.geoObjects.add(myGeoObject);
    }

    // Делегируем событие на весь документ, чтобы обработать клики по кнопкам в балунах
    document.addEventListener("click", function(event) {
        if (event.target.classList.contains("check-btn")) {
            showDialog(event.target.dataset.index);
        }
    });
}

async function loadObjects() {
    const user_id = document.getElementById("user_id").innerText;
    const url = `../admin/assignment/${user_id}`;

    try {
        let response = await fetch(url);
        let data = await response.json();
        console.log("Данные загружены:", data);
        objectsData = data;
        
    } catch (error) {
        console.error("Ошибка загрузки объектов:", error);
    }
}

// Функция для показа диалогового окна
function showDialog(index) {
    let dialog = document.getElementById("dialog");
    dialog.classList.add("show");
}

// Функция для скрытия диалогового окна
function closeDialog() {
    let dialog = document.getElementById("dialog");
    dialog.classList.remove("show");
}
function startCheck(){
    
}