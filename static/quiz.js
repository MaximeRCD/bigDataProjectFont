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
            const blob = new Blob(chunks, {'type': 'audio/wav'});
            const url = URL.createObjectURL(blob);

            const formData = new FormData();
            formData.append('audio', blob, 'audio.wav');
            formData.append('question_id', '1');
            formData.append('user_id', '1');
            console.log(formData);

            fetch('https://api-k3dvzrn44a-od.a.run.app/ml/prediction', {
                method: 'POST',
                body: formData
            }).then(function (data) {
                if (data.ok) {
                    console.log(data);
                    let icon = document.createElement('i');
                    icon.setAttribute('class', 'fe fe-mic');
                    recordButton.firstElementChild.remove();
                    recordButton.appendChild(icon);
                    modelResponse = data.predicted_label;

                    if (!document.getElementById(recordButton.getAttribute('answer_name') + data.predicted_label)) {
                        let toastEl = document.querySelector('.toast');
                        let toast = new bootstrap.Toast(toastEl);
                        toast.show();
                    } else {
                        document.getElementById(recordButton.getAttribute('answer_name') + data.predicted_label).checked = true;
                        document.getElementById('nextQ' + recordButton.getAttribute('answer_name')[1]).classList.remove('disabled');
                    }
                } else {
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
    const formData = new FormData(document.getElementById('quizForm'));
    const formEntries = Object.fromEntries(formData.entries());
    console.log(formEntries);
    questionNumber = parseInt(questionNumber, 10);

    for (let i = 1; i <= questionNumber; i++) {
        const questionKey = 'q' + i;
        const questionValue = formEntries[questionKey];
        console.log(`Valeur pour ${questionKey}: ${questionValue}`);
    }
    for (let i = 1; i <= questionNumber; i++) {
        const correctionKey = 'correctionQ' + i;
        if (correctionKey in formEntries) {
            const correctionValue = formEntries[correctionKey];
            console.log(`Valeur pour ${correctionKey}: ${correctionValue}`);
        }
    }
    window.location.href = 'results';
}

for (let i = 0; i < recordButtons.length; i++) {
    recordButtons[i].addEventListener('click', onRecordButtonClick);
}

for (let i = 0; i < answerButtons.length; i++) {
    answerButtons[i].addEventListener('click', onAnswerButtonClick);
}

