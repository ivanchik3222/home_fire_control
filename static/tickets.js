document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".form-section");
    
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Отменяем стандартную отправку формы
        
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: form.method,
            body: formData
        })
        .then(response => {
            if (response.ok) {
                let url = window.location.href.split("/");
                let assignmentId = url[url.length - 1]
                window.location.href = "/inspection/check_list/" + assignmentId; // Замените на нужный URL
            } else {
                return response.json().then(err => { throw new Error(err.message || 'Ошибка отправки'); });
            }
        })
        .catch(error => {
            alert("Ошибка: " + error.message);
        });
    });
});
