const sendBtn = document.getElementById("send-btn");
const messageInput = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");

sendBtn.addEventListener("click", sendMessage);

async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) return;

    chatBox.innerHTML += `
        <div class="user-message">
            ${message}
        </div>
    `;

    messageInput.value = "";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: message
                })
            }
        );

        const data = await response.json();

        chatBox.innerHTML += `
            <div class="ai-message">
                ${data.response}
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {

        chatBox.innerHTML += `
            <div class="ai-message">
                Backend bilan ulanishda xatolik.
            </div>
        `;
    }
}