window.baseUrl = 'http://test.igoose.ru:9999/';
// window.baseUrl = 'http://localhost:9999/';

document.addEventListener('DOMContentLoaded', function () {
    // Проверка наличия токена при загрузке страницы
    checkToken();
});

// Проверка токена при перезагрузке страницы
window.addEventListener('beforeunload', function (event) {
    // Выполнить проверку токена перед перезагрузкой страницы
    checkToken();
});


function checkToken() {
    // Получение токена из localStorage
    const accessToken = localStorage.getItem('access_token');
    console.log(accessToken)
    // Проверка наличия токена
    if (accessToken) {
        // Токен найден, выполните необходимые действия (например, вход в систему)
        console.log('Токен найден:', accessToken);
        if (window.location.pathname === '/') {
            redirectToFilePage()
        }
    } else {
        // Токен отсутствует, и проверяем, не произошло ли уже перенаправление
        if (window.location.pathname !== '/' && window.location.pathname !== '/signin') {
            // Перенаправление на страницу входа
            console.log('Токен отсутствует. Перенаправление на страницу входа.');
            window.location.href = `${window.baseUrl}`;
        }
    }
}


function submitForm() {
    // Получаем значения полей логина и пароля
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    const type = document.getElementById("next-button").innerText;

    // Формируем данные для отправки
    var formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    // Отправляем POST-запрос
    fetch(`${window.baseUrl}token`, {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            // Проверяем наличие токена в ответе
            if (data.access_token) {
                // Обработка данных, полученных от сервера
                console.log(data.access_token);

                // Сохраняем токен в локальном хранилище
                localStorage.setItem("access_token", data.access_token);
                // Переходим на другую страницу и передаем токен в заголовке запроса
                redirectToFilePage();
            } else {
                // Если токен не вернулся, запускаем функцию для регистрации
                console.log(type)
                if (type !== "Регестрация") {
                    registerUser();
                }
            }
        })
        .catch(error => {
            // Обработка ошибок
            console.error("Error:", error);
        });
}

function redirectToFilePage() {
    const authToken = localStorage.getItem("access_token");
    const redirectUrl = `${window.baseUrl}file?token=${authToken}`;
    window.location.href = redirectUrl
}


function registerUser() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Формируем объект с данными пользователя
    var userData = {
        login: username,
        password: password
    };

    fetch(`${window.baseUrl}user`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(userData)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (!data.detail) {
                submitForm();
            }
        })
        .catch(error => {
            // Обработка ошибок
            console.error("Error:", error);
        });
}

function toSignIns() {
    const url = `${window.baseUrl}signin`;
    window.location.href = url
}

function toReg() {
    const url = `${window.baseUrl}`;
    window.location.href = url
}
