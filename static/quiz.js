const recordButtons = document.getElementsByClassName('recordButton');
const answerButtons = document.getElementsByClassName('btn-check');
let recorder;
let stream;
let modelResponse, userResponse;

async function startRecording(recordButton) {
    stream = await navigator.mediaDevices.getUserMedia({audio: true});
    recorder = new MediaRecorder(stream);
    recorder.onstart = () => {
        let spinner = document.createElement('span');
        spinner.setAttribute('class', 'spinner-grow spinner-grow-sm text-danger');
        spinner.setAttribute('role', 'status');
        spinner.setAttribute('aria-hidden', 'true');
        recordButton.firstElementChild.remove();
        recordButton.appendChild(spinner);
    };
    recorder.start();
}

function onRecordButtonClick(event) {
    let recordButton = event.target;
    if (recordButton.tagName.toLowerCase() === 'span' || recordButton.tagName.toLowerCase() === 'i')
        recordButton = recordButton.parentNode;

    let spinner = document.createElement('span');
    spinner.setAttribute('class', 'spinner-border spinner-grow-sm text-light');
    spinner.setAttribute('role', 'status');
    spinner.setAttribute('aria-hidden', 'true');
    recordButton.firstElementChild.remove();
    recordButton.appendChild(spinner);

    if (!recorder || recorder.state !== 'recording') {
        startRecording(recordButton);
    } else if (recorder.state === 'recording') {
        recorder.stop();
        recorder.ondataavailable = (e) => {
            let chunks = [];
            chunks.push(e.data);
            const blob = new Blob(chunks, { 'type': 'audio/webm'});
            const url = URL.createObjectURL(blob);
            const formData = new FormData();
            formData.append('audio', blob, 'audio/webm');
            formData.append('question_id', '1');
            formData.append('user_id', '1');
            const entries = formData.entries();

            fetch('http://127.0.0.1:8001/ml/prediction', {
                method: 'POST',
                body: formData
            }).then(function (data) {
                if (data.ok) {
                    let icon = document.createElement('i');
                    icon.setAttribute('class', 'fe fe-mic');
                    recordButton.firstElementChild.remove();
                    recordButton.appendChild(icon);
                    data.json().then((result) => {
                        modelResponse = result.predicted_label;

                        if (!document.getElementById(recordButton.getAttribute('answer_name') + modelResponse)) {
                            let toastEl = document.querySelector('.toast');
                            let toast = new bootstrap.Toast(toastEl);
                            toast.show();
                        } else {
                            document.getElementById(recordButton.getAttribute('answer_name') + modelResponse).checked = true;
                            document.getElementById('nextQ' + recordButton.getAttribute('answer_name')[1]).classList.remove('disabled');
                        }
                    });

                } else {
                    console.log(data);
                    console.log('Upload failed');
                }
            }).catch(function (error) {
                console.log('Error uploading audio', error);
            });
        };
        stream.getTracks().forEach((track) => track.stop());
        recorder = null;
        stream = null;

    }
}

function onAnswerButtonClick(event) {
    if (modelResponse == null) {
        event.target.checked = false;
    } else {
        userResponse = event.target.getAttribute('id')[3];
        if (document.getElementById('correctionQ' + event.target.getAttribute('id')[1]))
            document.getElementById('correctionQ' + event.target.getAttribute('id')[1]).remove();
        let userCorrection = document.createElement('input');
        userCorrection.setAttribute('class', 'visually-hidden');
        userCorrection.setAttribute('id', 'correctionQ' + event.target.getAttribute('id')[1]);
        userCorrection.setAttribute('name', 'correctionQ' + event.target.getAttribute('id')[1]);
        userCorrection.setAttribute('value', modelResponse);
        event.target.parentNode.appendChild(userCorrection);
    }
}

function resetAnswer() {
    modelResponse = null;
    userResponse = null;
}

function finishQuiz(questionNumber) {
    let form = document.getElementById('quizForm');
    form.method = 'POST';
    form.action = 'create_quizz';
    form.onsubmit = null;
    form.submit();
    return 0;

    const formData = new FormData(form);
    console.log(formData);

    const formEntries = Object.fromEntries(formData.entries());
    const csrftoken = formEntries['csrfmiddlewaretoken'];
    delete formEntries['csrfmiddlewaretoken'];

    console.log(JSON.stringify(formEntries));

    /*questionNumber = parseInt(questionNumber, 10);
    let userResponse = '';

    for (let i = 1; i <= questionNumber; i++) {
        const questionKey = 'q' + i;
        const questionValue = formEntries[questionKey];
        userResponse += `"${questionKey}": "${questionValue}"`;
    }
    for (let i = 1; i <= questionNumber; i++) {
        const correctionKey = 'correctionQ' + i;
        if (correctionKey in formEntries) {
            const correctionValue = formEntries[correctionKey];
            console.log(`Valeur pour ${correctionKey}: ${correctionValue}`);
        }
    }*/

    fetch('create_quizz', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: {
            'str_response': JSON.stringify(formEntries)
        }
    }).then(function (data) {
        if (data.ok) {
            console.log(data);
            //window.location.href = 'results';
        }
        else {
            let toastEl = document.querySelector('.toast');
            let toast = new bootstrap.Toast(toastEl);
            toast.show();
        }
    });
}

for (let i = 0; i < recordButtons.length; i++) {
    recordButtons[i].addEventListener('click', onRecordButtonClick);
}

for (let i = 0; i < answerButtons.length; i++) {
    answerButtons[i].addEventListener('click', onAnswerButtonClick);
}

