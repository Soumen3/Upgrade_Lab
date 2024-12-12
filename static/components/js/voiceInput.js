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

        recognition.onstart = function () {
            console.log('Voice recognition started. Try speaking into the microphone.');
            micIcon.classList.add('mic-active');
            micIcon.innerHTML = `
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v4a1 1 0 102 0V7zm-1 8a3 3 0 01-3-3h2a1 1 0 002 0h2a3 3 0 01-3 3z" clip-rule="evenodd" />
            `;
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
            micIcon.innerHTML = `
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v4a1 1 0 102 0V7zm-1 8a3 3 0 01-3-3h2a1 1 0 002 0h2a3 3 0 01-3 3z" clip-rule="evenodd" />
            `;
        };

        voiceInputButton.addEventListener('click', function () {
            recognition.start();
        });
    } else {
        console.warn('Web Speech API is not supported by this browser.');
        voiceInputButton.disabled = true;
    }
});
