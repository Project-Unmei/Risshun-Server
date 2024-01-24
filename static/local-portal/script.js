console.log("Hello from local-portal/script.js");

function format_and_send_data(data, url="http://127.0.0.1:6969/api/cv/generate") {
    // Formatting final HTTP package
    let xhr = new XMLHttpRequest();
    let response;
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhr.setRequestHeader("X-API-KEY", "TESTAPIKEY");
    xhr.responseType = 'blob';
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            response = xhr.responseText;

            var binaryData = [];
            binaryData.push(response);

            var fileName = `${data.UID}.docx`;
            var a = document.createElement("a");
            a.href = window.URL.createObjectURL(new Blob(binaryData));
            a.download = fileName;
            a.click();

        }
    };

    // Sending JSON package to server
    xhr.send(JSON.stringify(data));
}

document.getElementById('info-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const gen_options = document.getElementsByName('gen-option');
    console.log(gen_options);

    // Find checked radio button
    let genChoice;
    for (const option of gen_options) {
        if (option.checked) {
            selectedValue = option.value;
            break;
        }
    }

    // Temporary overwrite, since only gpt is accepted
    selectedValue = "gpt";

    var formData = {
        UID: document.getElementById('uid').value,
        TYPE: selectedValue,
        DATA: {
            TITLE: document.getElementById('job-title').value,
            COMPANY: document.getElementById('job-company').value,
            JOB_SUM: document.getElementById('job-summary').value
        }
    };

    format_and_send_data(formData);
    console.log(formData)
    //var xhr = new XMLHttpRequest();
    //xhr.open("POST", "http://localhost:YOUR_PORT", true);
    //xhr.setRequestHeader("Content-Type", "application/json");
    //xhr.send(jsonData);
});
