document.addEventListener("DOMContentLoaded", function () {
    fetchNotifications();
});

function toggleNotifications() {
    const container = document.getElementById("notifications-container");
    if (container.style.display === "none" || container.style.display === "") {
        fetchNotifications(); // Загружаем уведомления перед открытием
        container.style.display = "block";
    } else {
        container.style.display = "none";
    }
}

function fetchNotifications() {
    fetch("/inspection/get_notifications")
        .then(response => response.json())
        .then(data => {
            const notificationsList = document.getElementById("notifications-list");
            notificationsList.innerHTML = "";

            if (data.notifications.length === 0) {
                notificationsList.innerHTML = "<li>Нет новых уведомлений</li>";
                return;
            }

            data.notifications.forEach(notification => {
                const listItem = document.createElement("li");
                listItem.textContent = `${notification.message} (${notification.created_at})`;
                notificationsList.appendChild(listItem);
            });
        })
        .catch(error => console.error("Ошибка загрузки уведомлений:", error));
}
