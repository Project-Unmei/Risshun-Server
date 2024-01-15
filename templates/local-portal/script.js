document.getElementById('dataForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value
    };

    var jsonData = JSON.stringify(formData);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:YOUR_PORT", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(jsonData);
});
