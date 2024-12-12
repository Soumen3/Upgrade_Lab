document.addEventListener('DOMContentLoaded', function () {
    const voiceInputButton = document.getElementById('voiceInput');
    const promptInput = document.getElementById('prompt');
    const micIcon = voiceInputButton.querySelector('svg');

    // Check if the browser supports the Web Speech API
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        let isListening = false;

        recognition.onstart = function () {
            console.log('Voice recognition started. Try speaking into the microphone.');
            micIcon.classList.add('mic-active');
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            promptInput.value = transcript;
            console.log('Voice recognition result: ', transcript);
        };

        recognition.onerror = function (event) {
            console.error('Voice recognition error: ', event.error);
        };

        recognition.onend = function () {
            console.log('Voice recognition ended.');
            micIcon.classList.remove('mic-active');
            isListening = false;
        };

        voiceInputButton.addEventListener('click', function () {
            if (isListening) {
                recognition.stop();
            } else {
                recognition.start();
                isListening = true;
            }
        });
    } else {
        console.warn('Web Speech API is not supported by this browser.');
        voiceInputButton.disabled = true;
    }
});
