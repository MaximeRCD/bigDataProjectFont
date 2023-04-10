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
    let recordButton = event.target; // L'objet qui a déclenché l'événement
    if (recordButton.tagName.toLowerCase() === 'span' || recordButton.tagName.toLowerCase() === 'i')
        recordButton = recordButton.parentNode;

    if (!recorder || recorder.state !== 'recording') {
        startRecording(recordButton);
    } else if (recorder.state === 'recording') {
        recorder.stop();
        recorder.ondataavailable = (e) => {
            const audioURL = URL.createObjectURL(e.data);
            console.log(audioURL);
        };
        stream.getTracks().forEach((track) => track.stop());
        recorder = null;
        stream = null;
        fetch('/fake_model/')
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Erreur HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                let icon = document.createElement('i');
                icon.setAttribute('class', 'fe fe-mic');
                recordButton.firstElementChild.remove();
                recordButton.appendChild(icon);
                modelResponse = data.answer;

                if (!document.getElementById(recordButton.getAttribute('answer_name') + data.answer)){
                    let toastEl = document.querySelector('.toast');
                    let toast = new bootstrap.Toast(toastEl);
                    toast.show();
                }
                else {
                    document.getElementById(recordButton.getAttribute('answer_name') + data.answer).checked = true;
                    document.getElementById('nextQ'+recordButton.getAttribute('answer_name')[1]).classList.remove('disabled');
                }
            })
            .catch((error) => {
                console.error('Erreur lors de la requête à l\'API:', error);
            });
    }
}

function onAnswerButtonClick(event) {
    if (modelResponse == null) {
        event.target.checked = false;
    }
    else {
        const answerButton = event.target;
        userResponse = answerButton.id[-1];
    }
}

for (let i = 0; i < recordButtons.length; i++) {
    recordButtons[i].addEventListener('click', onRecordButtonClick);
}

for (let i = 0; i < answerButtons.length; i++) {
    answerButtons[i].addEventListener('click', onAnswerButtonClick);
}