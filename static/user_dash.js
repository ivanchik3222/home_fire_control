let objectsData = [];



function loadObjects() {
    const user_id = document.getElementById("user_id").innerText;
    const url = `../admin/assignment/${user_id}`;

    fetch(url) // Эндпоинт для получения списка объектов
        .then(response => response.json())
        .then(data => {
            objectsData = data;
            console.log(objectsData)
            updateTaskTable()
        })
        .catch(error => console.error("Ошибка загрузки объектов:", error));
}


loadObjects()


function updateTaskTable() {
    const mainElement = document.querySelector('main');

    // Удаляем ранее добавленные блоки container-image и free-text, если они есть
    const existingBlocks = mainElement.querySelectorAll('.container-image, .free-text');
    existingBlocks.forEach(block => block.remove());

    const tableBody = document.querySelector('.task-table tbody');
    tableBody.innerHTML = ''; // Очищаем таблицу

    // Фильтруем объекты: исключаем те, у которых status равен 'completed'
    const filteredData = objectsData.filter(obj => obj.status !== 'completed');

    if (filteredData.length === 0) {
        // Если объектов для проверки нет, добавляем элементы после заголовка
        const containerImage = document.createElement('div');
        containerImage.className = 'container-image';

        const freeText = document.createElement('div');
        freeText.className = 'free-text';
        freeText.textContent = 'Нет объектов для проверки';

        // Вставляем блоки после заголовка h1
        const title = document.querySelector('.task-title');
        title.insertAdjacentElement('afterend', containerImage);
        containerImage.insertAdjacentElement('afterend', freeText);
    } else {
        // Если объекты есть, заполняем таблицу
        filteredData.forEach(obj => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <div class="row">
                        <span>${obj.name}</span>
                        <button class="work-btn" onclick="takeTask(${obj.assigment_id})">Взять в работу</button>
                    </div>
                </td>
            `;
            tableBody.appendChild(row);
        });
    }
}



function takeTask(assigment_id) {
    const oldUrl = window.location.href;
    const newUrl = oldUrl.replace("/dashboard", `/way_map/${assigment_id}`);
    window.location.href = newUrl;
}

// Автоматическое обновление таблицы раз в 30 секунд
setInterval(updateTaskTable, 30000);

// Первоначальная загрузка
document.addEventListener('DOMContentLoaded', updateTaskTable);