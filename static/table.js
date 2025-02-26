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
    const tableBody = document.getElementById("projectsTableBody_");
    tableBody.innerHTML = "";
    
    const visibleProjects = projectsData.slice(currentIndex, currentIndex + rowsPerPage);
    for (let i = 0; i < rowsPerPage; i++) {
      let project = visibleProjects[i] || { name: "", status: "", date: "" };
      let row = `<tr>
                  <td>${project.name}</td>
                  <td>${project.status}</td>
                  <td>${project.date}</td>
                </tr>`;
      tableBody.innerHTML += row;
    }
    
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
        let object = visibleObjects[i] || { name: "", category: "", date: "" };
        let row = `<tr>
                    <td>${object.name}</td>
                    <td>${object.category}</td>
                    <td>${object.date}</td>
                </tr>`;
        tableBody.innerHTML += row;
    }
    updateObjectButtons()
    function updateObjectButtons() {
        document.getElementById("prevObjectButton").style.opacity = objectIndex === 0 ? "0.5" : "1";
        document.getElementById("prevObjectButton").disabled = objectIndex === 0;
        document.getElementById("nextObjectButton").style.opacity = objectIndex + objectsPerPage >= objectsData.length ? "0.5" : "1";
        document.getElementById("nextObjectButton").disabled = objectIndex + objectsPerPage >= objectsData.length;
    }
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
document.getElementById("backToObjects_").addEventListener("click", function () {
    document.getElementById("addObjectModal_").style.display = "none";
    document.getElementById("objectsModal_").style.display = "block";
    document.getElementById("modalOverlay_").style.display = "flex";
    document.getElementById("userInfo_").style.display = "none";
    loadObjects(); // Перезагрузка списка объектов
});




document.getElementById("addObjectButton_").addEventListener("click", function () {
    document.getElementById("modalOverlay_").style.display = "flex";
    document.getElementById("addObjectModal_").style.display = "block";
    document.getElementById("objectsModal_").style.display = "none";
    document.getElementById("userInfo_").style.display = "none";

    let addObjectModal = document.createElement("div");
    addObjectModal.classList.add("modal_");
    addObjectModal.innerHTML = `
        <div class="modal-header_">
            <h2>Добавить объект</h2>
            <span class="close-btn_" id="closeAddObjectModal_">&times;</span>
        </div>
        <form class="modal-content_" id="addObjectForm">
            <label for="object_address">Адрес:</label>
            <input type="text" id="object_address" required placeholder="Введите адрес">
            <label for="object_coordinates">Координаты:</label>
            <input type="text" id="object_coordinates" required placeholder="Введите координаты">
            <label for="object_type">Тип объекта:</label>
            <input type="text" id="object_type" required placeholder="Введите тип объекта">
            <button type="submit">Добавить объект</button>
        </form>
    `;

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
            loadObjects(); // Обновление списка объектов
        })
        .catch(error => console.error("Ошибка:", error));
    });
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
