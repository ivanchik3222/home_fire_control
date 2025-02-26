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

document.querySelectorAll(".details-button").forEach(button => {
    button.addEventListener("click", function () {
      // Получаем данные пользователя из атрибутов кнопки
      const userData = JSON.parse(this.getAttribute("data-user"));
      // Заполняем модальное окно данными
      document.getElementById("profilePic_").src = userData.profile_picture || "../../static/materials/default.png";
      document.getElementById("firstName_").innerText = userData.first_name;
      document.getElementById("lastName_").innerText = userData.last_name;
      document.getElementById("middleName_").innerText = userData.middle_name;

      // Заполняем таблицу проектов
      let projectsTable = document.getElementById("projectsTableBody_");
      projectsTable.innerHTML = "";
      userData.projects.forEach(project => {
        let row = `<tr>
                    <td>${project.name}</td>
                    <td>${project.status}</td>
                    <td>${project.date}</td>
                  </tr>`;
        projectsTable.innerHTML += row;
      });

      // Показываем модальное окно
      document.getElementById("modalOverlay_").style.display = "flex";
    });
  });

  // Закрытие модального окна
  document.getElementById("closeModal_").addEventListener("click", function () {
    document.getElementById("modalOverlay_").style.display = "none";
  });