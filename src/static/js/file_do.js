window.baseUrl = 'http://test.igoose.ru:9999/';
// window.baseUrl = 'http://localhost:9999/';

function userExit() {
    console.log("User exit")
    try {
        localStorage.clear();
        const url = `${window.baseUrl}signin`
        window.location.href = url
    } catch (error) {
        console.error("Произошла ошибка: ", error);
    }
}

function toMenu() {
    const url = `${window.baseUrl}`
    window.location.href = url
}

function toAdd() {
    const url = `${window.baseUrl}add`
    window.location.href = url
}

function toSheets(filename) {
    const authToken = localStorage.getItem("access_token");
    const url = `${window.baseUrl}file/${filename}?token=${authToken}`;
    window.location.href = url
}

function toRandom(filename, sheetname) {
    const authToken = localStorage.getItem("access_token");
    const url = `${window.baseUrl}file/${filename}/${sheetname}?token=${authToken}`;
    window.location.href = url
}

function deleteFile(filename) {
    const authToken = localStorage.getItem("access_token");
    const url = `${window.baseUrl}file/${filename}?token=${authToken}`;

    fetch(url, {
        method: "DELETE",
    })
        .then(resp => {
            if (!resp.ok) {
                console.log(resp.status);
            } else {
                toMenu();
            }
        })
        .catch(error => {
            console.error(error);
        });
}

function updateQ() {
    const id = document.getElementById("info-id")
    const intValue = parseInt(id.innerText, 10);
    const filename = document.getElementById("filename")
    const sheet = document.getElementById("sheet")

    const repFileName = filename.innerText.split(":")
    const repSheet = sheet.innerText.split(":")

    const authToken = localStorage.getItem("access_token");
    const url = `${window.baseUrl}file/${repFileName[repFileName.length - 1].slice(1)}/${repSheet[repSheet.length - 1].slice(1)}/${intValue}?token=${authToken}`;

    fetch(url, {
        method: "DELETE"
    })
        .then(resp => {
            if (!resp.ok) {
                console.log(resp.status);
            } else {
                window.location.reload();
            }
        })
        .catch(error => {
            console.error(error);
        });

}