function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value;

    if (message.trim() === "") return;

    addMessage("You: " + message);

    fetch("/ask", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        addMessage("NIRIA: " + data.reply);
        speak(data.reply);
    });

    input.value = "";


};

    


function addMessage(text) {
    let chat = document.getElementById("chat-window");
    chat.innerHTML += "<div>" + text + "</div>";
    chat.scrollTop = chat.scrollHeight;
}

function speak(text) {
    let speech = new  SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    window.speechSynthesis.speak(speech);
}

function startListening() {
    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function(event) {
        document.getElementById("user-input").value = event.results[0][0].transcript;
        sendMessage();
    };
}