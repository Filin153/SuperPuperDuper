window.baseUrl = 'http://localhost:9999/';

function loadFile() {
    const fileInput = document.getElementById('fileInput');
    const authToken = localStorage.getItem("access_token");
    const url = `${window.baseUrl}file?token=${authToken}`;

    if (fileInput.files.length > 0) {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        // Display loading indicator
        showLoadingIndicator();

        // Send file to server using fetch
        fetch(url, {
            method: 'POST',
            body: formData,
        })
            .then(response => {
                // Handle response from server
                console.log(response.ok);
                if (!response.ok) {
                    throw new Error("Answer != ok")
                }

                hideLoadingIndicator();
            })
            .catch(error => {
                console.error('Error uploading file:', error);

                // Hide loading indicator on error
                hideLoadingIndicator();
            });
    }
}

function showLoadingIndicator() {
    const loadingIndicator = document.getElementById('loadingIndicator');
    loadingIndicator.style.display = 'block';
}

function hideLoadingIndicator() {
    const loadingIndicator = document.getElementById('loadingIndicator');
    loadingIndicator.style.display = 'none';
}
