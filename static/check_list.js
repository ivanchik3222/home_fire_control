document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.checklist-form');
    console.log("init");
    console.log(form);
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(form);

        // Собираем данные для критериев: включаем все, кроме поля заключения, user_id и admin_id
        let criteriaData = {
            assigment_id: formData.get('assigment_id'),
            functional_fire_risk: formData.get('functional_fire_risk'),
            risk_score: formData.get('risk_score'),
            answers: {}
        };
        
        for (const [key, value] of formData.entries()) {
            if (!["assigment_id", "functional_fire_risk", "risk_score"].includes(key)) {
                criteriaData.answers[key] = value;
            }
        }
        
        console.log(criteriaData)
        let url = window.location.href.split("/");
        let assignmentId = url[url.length - 1];
        criteriaData['assigment_id'] = assignmentId;
        // Отправляем данные критериев на /form/create в формате JSON
        fetch('/inspection/form/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(criteriaData)
        })
        .then(response => {
            if (!response.ok) {

                throw new Error('Ошибка при отправке данных формы');
            }
            return response.json();
        })
        .then(result => {
            let url = window.location.href.split("/");
            let assignmentId = url[url.length - 1];
            // После успешной отправки критериев, собираем данные из блока заключения
            const conclusion = formData.get('conclusion');
            const conclusionData = {
                fire_risk_level: conclusion, // В роуте create_result поле называется fire_risk_level
                assigment_id: assignmentId,
                user_id: formData.get('user_id'),
                admin_id: formData.get('admin_id'),
            };
            console.log(conclusionData)
            return fetch('/inspection/result/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(conclusionData)
            });
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка при отправке заключения');
            }
            return response.json();
        })
        .then(result => {
            alert('Данные успешно отправлены!');
            window.location.href = '/inspection/dashboard'
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert(error.message);
        });
    });
});