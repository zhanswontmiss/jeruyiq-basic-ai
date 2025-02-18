document.addEventListener("DOMContentLoaded", function() {
    const chatInput = document.querySelector(".chat-input");
    const sendButton = document.querySelector(".send-button");
    const chatBox = document.querySelector(".chat-box");

    function appendMessage(text, sender) {
        let messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);
        messageDiv.innerText = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        appendMessage(`You: ${message}`, "user");
        chatInput.value = "Thinking...";

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            chatInput.value = "";
            appendMessage(`AI: ${data.response}`, "ai");
        } catch (error) {
            appendMessage("Error: Could not reach server", "error");
        }
    }

    sendButton.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});