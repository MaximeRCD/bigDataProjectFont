const recordButtons = document.getElementsByClassName('recordButton');
const answerButtons = document.getElementsByClassName('btn-check');
let recorder;
let stream;
let modelResponse, userResponse;

const mapping = {
    "un": 1,
    "deux": 2,
    "trois": 3,
    "quatre": 4,
    "oui": 1,
    "non": 2
};

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

            const formData = new FormData();
            formData.append('audio', blob, 'audio/webm');
            formData.append('question_id', recordButton.getAttribute('answer_name').replace('a', '').replace('q', ''));
            formData.append('user_id', document.getElementById('user_id').textContent);
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
                        console.log(result);
                        modelResponse = mapping[result.predicted_label];

                        if (document.getElementById('correction_' + recordButton.getAttribute('answer_name').replace('a', '')))
                            document.getElementById('correction_' + recordButton.getAttribute('answer_name').replace('a', '')).remove();
                        let userCorrection = document.createElement('input');
                        userCorrection.setAttribute('class', 'visually-hidden');
                        userCorrection.setAttribute('id', 'correction_' + recordButton.getAttribute('answer_name').replace('a', ''));
                        userCorrection.setAttribute('name', 'correction_' + recordButton.getAttribute('answer_name').replace('a', ''));
                        if (document.getElementById(recordButton.getAttribute('answer_name') + modelResponse).getAttribute('data-type-question') === "truefalse")
                            if (modelResponse === 1)
                                userCorrection.setAttribute('value', "oui");
                            else
                                userCorrection.setAttribute('value', "non");
                        else
                            userCorrection.setAttribute('value', modelResponse);
                        document.getElementById(recordButton.getAttribute('answer_name') + modelResponse).parentNode.appendChild(userCorrection);

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
        const regex = /a(\d+)/;
        const match = event.target.getAttribute('id').match(regex);

        if (match) {
            userResponse = match[1];
        } else {
            console.log("No match found.");
        }
        if (document.getElementById('correction_' + event.target.getAttribute('name')))
            document.getElementById('correction_' + event.target.getAttribute('name')).remove();
        let userCorrection = document.createElement('input');
        userCorrection.setAttribute('class', 'visually-hidden');
        userCorrection.setAttribute('id', 'correction_' + event.target.getAttribute('name'));
        userCorrection.setAttribute('name', 'correction_' + event.target.getAttribute('name'));
        if (event.target.getAttribute('data-type-question') === "truefalse")
            if (modelResponse === 1)
                userCorrection.setAttribute('value', "oui");
            else
                userCorrection.setAttribute('value', "non");
        else
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
