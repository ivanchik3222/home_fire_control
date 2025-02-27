function add_user() {
    // Создание модального окна
    let modal = document.createElement("div");
    modal.classList.add("modal");
    modal.innerHTML = `
        <div class="modal-header">
            <h2>Добавить пользователя</h2>
            <span class="close-button">&times;</span>
        </div>
        <form class="modal-content" onsubmit="sendUserData(event)">
            <label for="full_name">ФИО:</label>
            <input type="text" id="full_name" required placeholder="Введите ФИО">
            <label for="login">Логин:</label>
            <input type="text" id="login" required placeholder="Введите логин">
            <label for="password">Пароль:</label>
            <input type="password" id="password" required placeholder="Введите пароль">
            <button>Добавить</button>
        </form>
    `;
    document.body.appendChild(modal);

    // Закрытие модального окна
    document.querySelector(".close-button").onclick = function () {
        modal.remove();
    };

    makeDraggable(modal);
}
function sendUserData(event) {
    event.preventDefault();
    let full_name = document.getElementById("full_name").value;
    let login = document.getElementById("login").value;
    let password = document.getElementById("password").value;
    const body = JSON.stringify({ full_name, login, password });
    fetch("user/create", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: body
    })
    .then(response => response.text())
    .then(data => {
        alert("Пользователь успешно добавлен!");
        document.querySelector(".modal").remove();
        location.reload();
    })
    .catch(error => console.error("Ошибка:", error));
}
// Функция для перетаскивания окна
function makeDraggable(element) {
    let header = document.querySelector(".modal-header");
    let offsetX = 0, offsetY = 0, isDragging = false;

    header.onmousedown = function(event) {
        isDragging = true;
        offsetX = event.clientX - element.offsetLeft;
        offsetY = event.clientY - element.offsetTop;

        document.onmousemove = function(event) {
            if (isDragging) {
                element.style.left = event.clientX - offsetX + "px";
                element.style.top = event.clientY - offsetY + "px";
            }
        };

        document.onmouseup = function() {
            isDragging = false;
            document.onmousemove = null;
            document.onmouseup = null;
        };
    };
}
let currentIndex = 0;
const rowsPerPage = 3;
let projectsData = [];

function updateTable() {
    const user_id = document.getElementById("user_id").innerText;

    const url = "assignment/" + user_id;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            projectsData = data; // Сохраняем загруженные данные
            renderTable(); // Рендерим таблицу после загрузки данных
        })
        .catch(error => console.error("Ошибка создания назначения:", error));
}

function renderTable() {
    const tableBody = document.getElementById("projectsTableBody_");
    tableBody.innerHTML = "";

    const visibleProjects = projectsData.slice(currentIndex, currentIndex + rowsPerPage);
    
    visibleProjects.forEach(project => {
        let row = `<tr>
                      <td>${project.name || "—"}</td>
                      <td>${project.status || "—"}</td>
                      <td>${project.date || "—"}</td>
                   </tr>`;
        tableBody.innerHTML += row;
    });

    updateButtons();
}

function updateButtons() {
document.getElementById("prevButton").style.opacity = currentIndex === 0 ? "0.7" : "1";
document.getElementById("prevButton").disabled = currentIndex === 0;
document.getElementById("nextButton").style.opacity = currentIndex + rowsPerPage >= projectsData.length ? "0.7" : "1";
document.getElementById("nextButton").disabled = currentIndex + rowsPerPage >= projectsData.length;
}

document.getElementById("prevButton").addEventListener("click", function () {
if (currentIndex > 0) {
    currentIndex -= rowsPerPage;
    updateTable();
}
});

document.getElementById("nextButton").addEventListener("click", function () {
if (currentIndex + rowsPerPage < projectsData.length) {
    currentIndex += rowsPerPage;
    updateTable();
}
});

document.querySelectorAll(".details-button").forEach(button => {
button.addEventListener("click", function () {
    const userData = JSON.parse(this.getAttribute("data-user"));
    document.getElementById("profilePic_").src = userData.profile_picture || "../../static/materials/default.png";
    document.getElementById("firstName_").innerText = userData.first_name;
    document.getElementById("lastName_").innerText = userData.last_name;
    document.getElementById("middleName_").innerText = userData.middle_name;
    document.getElementById("user_id").innerText = userData.user_id
    
    projectsData = userData.projects;
    currentIndex = 0;
    updateTable();
    
    document.getElementById("modalOverlay_").style.display = "flex";
    document.getElementById("userInfo_").style.display = "block";
});
});

document.getElementById("closeModal_").addEventListener("click", function () {
document.getElementById("modalOverlay_").style.display = "none";
document.getElementById("userInfo_").style.display = "none";
});


let objectIndex = 0;
const objectsPerPage = 3;
let objectsData = [];
function updateObjectsTable() {
    const tableBody = document.getElementById("objectsTableBody_");
    tableBody.innerHTML = "";

    const visibleObjects = objectsData.slice(objectIndex, objectIndex + objectsPerPage);
    for (let i = 0; i < objectsPerPage; i++) {
        // Если данных нет, задаём пустые значения
        let object = visibleObjects[i] || { id: "", address: "", type: "", coordinates: "" };
        let row = `<tr>
                    <td>${object.address}</td>
                    <td>${object.type}</td>
                    <td>
                      <button class="button_top assign-button"
                              data-object-id="${object.id}"
                              data-address="${object.address}"
                              data-type="${object.type}"
                              data-coordinates="${object.coordinates}">&rarr;</button>
                    </td>
                </tr>`;
        tableBody.innerHTML += row;
    }
    updateObjectButtons();

    function updateObjectButtons() {
        document.getElementById("prevObjectButton").style.opacity = objectIndex === 0 ? "0.5" : "1";
        document.getElementById("prevObjectButton").disabled = objectIndex === 0;
        document.getElementById("nextObjectButton").style.opacity = objectIndex + objectsPerPage >= objectsData.length ? "0.5" : "1";
        document.getElementById("nextObjectButton").disabled = objectIndex + objectsPerPage >= objectsData.length;
    }
    document.querySelectorAll(".assign-button").forEach(button => {
        button.addEventListener("click", function () {
            const objectId = this.dataset.objectId;
            // Записываем выбранный object_id в скрытое поле формы
            document.getElementById("assign_object_id").value = objectId;
            // Дополнительно можно, например, вывести данные объекта в окно (если нужно)
            // document.getElementById("assignObjectInfo").innerText = `Адрес: ${this.dataset.address}, Тип: ${this.dataset.type}`;

            // Скрываем окно объектов и показываем окно назначения
            document.getElementById("objectsModal_").style.display = "none";
            document.getElementById("assignObjectModal_").style.display = "block";
        });
    });
}

document.getElementById("prevObjectButton").addEventListener("click", function () {
if (objectIndex > 0) {
    objectIndex -= objectsPerPage;
    updateObjectsTable();
}
});

document.getElementById("nextObjectButton").addEventListener("click", function () {
if (objectIndex + objectsPerPage < objectsData.length) {
    objectIndex += objectsPerPage;
    updateObjectsTable();
}
});

document.getElementById("backToUserInfo_").addEventListener("click", function () {
    document.getElementById("objectsModal_").style.display = "none";
    document.getElementById("modalOverlay_").style.display = "flex";
    document.getElementById("userInfo_").style.display = "block";
});

document.getElementById("closeObjectsModal_").addEventListener("click", function () {
    document.getElementById("objectsModal_").style.display = "none";
    document.getElementById("modalOverlay_").style.display = "none";
    document.getElementById("userInfo_").style.display = "none";
});
document.getElementById("viewObjects_").addEventListener("click", function () {
    document.getElementById("objectsModal_").style.display = "block";
    document.getElementById("modalOverlay_").style.display = "flex";
    document.getElementById("userInfo_").style.display = "none";
});
function backToObjects(){
    document.getElementById("addObjectModal_").style.display = "none";
    document.getElementById("objectsModal_").style.display = "block";
    document.getElementById("modalOverlay_").style.display = "flex";
    document.getElementById("userInfo_").style.display = "none";
    document.getElementById("assignObjectModal_").style.display = "none";
    loadObjects(); // Перезагрузка списка объектов
}
document.getElementById("backToObjects_").addEventListener("click", function () {
    backToObjects()
});

document.getElementById("addObjectButton_").addEventListener("click", function () {
    document.getElementById("modalOverlay_").style.display = "flex";
    document.getElementById("addObjectModal_").style.display = "block";
    document.getElementById("objectsModal_").style.display = "none";
    document.getElementById("userInfo_").style.display = "none";

    // Обработчик формы добавления объекта
    document.getElementById("addObjectForm").addEventListener("submit", function (event) {
        event.preventDefault();
        let objectAddress = document.getElementById("object_address").value;
        let objectCoordinates = document.getElementById("object_coordinates").value;
        let objectType = document.getElementById("object_type").value;

        let formData = new FormData();
        formData.append("address", objectAddress);
        formData.append("coordinates", objectCoordinates);
        formData.append("type", objectType);

        fetch("object/create", {
            method: "POST",
            body: formData,
            credentials: "include" // Если используется Flask-Login
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            document.getElementById("addObjectModal_").style.display = "none";
            document.getElementById("objectsModal_").style.display = "block";
            document.getElementById("modalOverlay_").style.display = "flex";
            document.getElementById("userInfo_").style.display = "none";
            document.getElementById("object_address").value = "";
            document.getElementById("object_coordinates").value = "";
            document.getElementById("object_type").value = "";
            loadObjects(); // Обновление списка объектов
        })
        .catch(error => console.error("Ошибка:", error));
    });
});

document.getElementById("closeAssignObjectModal_").addEventListener("click", function () {
    document.getElementById("assignObjectModal_").style.display = "none";
    document.getElementById("objectsModal_").style.display = "none";
    document.getElementById("modalOverlay_").style.display = "none";
});

// Обработчик отправки формы назначения
document.getElementById("assignObjectForm").addEventListener("submit", function (event) {
    event.preventDefault();
    const user_id = document.getElementById("user_id").innerText;
    console.log(user_id)
    const objectId = document.getElementById("assign_object_id").value;
    const notificationMessage = document.getElementById("notification_message").value;
    
    // Формируем данные для отправки
    const payload = {
        user_id: user_id,
        object_id: objectId,
        message: notificationMessage
    };
    
    fetch("assignment/create", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload),
        credentials: "include" // если используется авторизация через Flask-Login
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        // Закрываем окно назначения и возвращаем окно со списком объектов
        document.getElementById("assignObjectModal_").style.display = "none";
        document.getElementById("objectsModal_").style.display = "block";
        // Обновляем список объектов, если необходимо
        loadObjects();
    })
    .catch(error => console.error("Ошибка создания назначения:", error));
});

// Функция для загрузки списка объектов после добавления нового
function loadObjects() {
    fetch("objects") // Эндпоинт для получения списка объектов
        .then(response => response.json())
        .then(data => {
            objectsData = data.objects;
            updateObjectsTable();
        })
        .catch(error => console.error("Ошибка загрузки объектов:", error));
}
loadObjects()
