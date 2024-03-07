window.baseUrl = 'http://localhost:9999/';

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

function updateQ() {
    const id = document.getElementById("num-q")
    const que = document.getElementById("text-q")
    const intValue = parseInt(id.innerText, 10);
    const filename = document.getElementById("filename")
    const sheet = document.getElementById("sheet")

    const repFileName = filename.innerText.split(":")
    const repSheet = sheet.innerText.split(":")

    const authToken = localStorage.getItem("access_token");
    const url = `${window.baseUrl}file/${repFileName[repFileName.length - 1].slice(1)}/${repSheet[repSheet.length - 1].slice(1)}/${intValue}?token=${authToken}&que=${que.innerText}`;

    fetch(url, {
        method: "DELETE"
    })
        .then(resp => {
            if (!resp.ok) {
                console.log(resp.status)
                throw new Error("Status code != 200")
            } else {
                window.location.reload()
            }
        })
        .catch(error => {
            console.error(error)
        })
}