const recordButtons = document.getElementsByClassName('recordButton');
const audioPlayer = document.getElementById('audioPlayer');

let recorder;
let stream;

async function startRecording(recordButton) {
    stream = await navigator.mediaDevices.getUserMedia({audio: true});
    recorder = new MediaRecorder(stream);
    recorder.onstart = () => {
        recordButton.innerHTML = '<span class="spinner-grow spinner-grow-sm text-danger" role="status" aria-hidden="true"></span>';
    };
    recorder.start();
}

function onRecordButtonClick(event) {
    const recordButton = event.target; // L'objet qui a déclenché l'événement
    if (!recorder || recorder.state !== 'recording') {
        startRecording(recordButton);
    } else if (recorder.state === 'recording') {
        recorder.stop();
        recordButton.innerHTML = '';
        recordButton.innerHTML = '<i class="fe fe-mic"></i>';
        recorder.ondataavailable = (e) => {
            const audioURL = URL.createObjectURL(e.data);
            console.log(audioURL);
        };
        stream.getTracks().forEach((track) => track.stop());
        fetch('/fake_model/')
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Erreur HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                console.log(data);
                document.getElementById(recordButton.getAttribute('answer_name') + data.answer).checked = true;
            })
            .catch((error) => {
                console.error('Erreur lors de la requête à l\'API:', error);
            });
    }
}

for (let i = 0; i < recordButtons.length; i++) {
    recordButtons[i].addEventListener('click', onRecordButtonClick);
}