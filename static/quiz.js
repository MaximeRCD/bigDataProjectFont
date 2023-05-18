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

            fetch('https://api-k3dvzrn44a-od.a.run.app/ml/prediction', {
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
                            document.getElementById('nextQ' + recordButton.getAttribute('answer_name').replace('q', '').replace('a', '')).classList.remove('disabled');
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
        userCorrection.setAttribute('id', event.target.getAttribute('name'));
        userCorrection.setAttribute('name', event.target.getAttribute('name'));
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
}

for (let i = 0; i < recordButtons.length; i++) {
    recordButtons[i].addEventListener('click', onRecordButtonClick);
}

for (let i = 0; i < answerButtons.length; i++) {
    answerButtons[i].addEventListener('click', onAnswerButtonClick);
}

document.addEventListener('DOMContentLoaded', function() {
    if (window.location.href.includes('themes')) {
        const form = document.querySelector('#create_quiz_form');
        const checkboxes = document.querySelectorAll('input[name^="theme"]');
        const submitButton = document.querySelector('#create_quiz');

        form.addEventListener('submit', function(event) {
            const selectedThemes = Array.from(checkboxes).filter(checkbox => checkbox.checked);

            if (selectedThemes.length === 0 || selectedThemes.length > 3) {
                event.preventDefault(); // Bloque l'envoi du formulaire
            }
        });

        checkboxes.forEach(function(checkbox) {
            checkbox.addEventListener('change', function() {
                const selectedThemes = Array.from(checkboxes).filter(checkbox => checkbox.checked);
                if (selectedThemes.length === 0 || selectedThemes.length > 3) {
                    submitButton.classList.add('disabled');
                } else {
                    submitButton.classList.remove('disabled');
                }
            });
        });
    }
});
