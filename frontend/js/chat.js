// chat.js - Customer chat logic

document.addEventListener('DOMContentLoaded', () => {
    // Check if user is authenticated
    const user = window.auth.checkAuth();
    if (!user) return;

    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatBox = document.getElementById('chat-box');
    const sendBtn = document.getElementById('send-btn');

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            // Display user message
            appendMessage(message, 'user');
            chatInput.value = '';
            chatInput.disabled = true;
            sendBtn.disabled = true;

            // Display typing indicator
            const typingId = appendTypingIndicator();

            try {
                // Determine if it's a purchase intent based on user prompt rules
                const isPurchaseIntent = /olaman|ha|sotib olaman|olib ber/i.test(message);

                // Assuming the backend has a /chat endpoint that expects { message }
                const response = await window.api.fetch('/chat', {
                    method: 'POST',
                    body: JSON.stringify({ message: message })
                });

                removeTypingIndicator(typingId);
                
                // Extract response text and potentially product recommendations
                // Handling depends on how FastAPI returns the data.
                // Assuming standard format: { reply: "text", recommended_product: { name: "", category: "", price: 0, color: "", size: "" } }
                
                let aiReply = response.reply || response.response || response.message || JSON.stringify(response);
                
                appendMessage(aiReply, 'ai', response.recommended_product || response.product);

            } catch (error) {
                removeTypingIndicator(typingId);
                appendMessage('Xatolik yuz berdi: ' + error.message, 'ai');
            } finally {
                chatInput.disabled = false;
                sendBtn.disabled = false;
                chatInput.focus();
            }
        });
    }

    function appendMessage(text, sender, product = null) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-message message-${sender}`;
        
        // Convert plain text to HTML (basic newlines to <br>)
        let htmlContent = `<div>${text.replace(/\\n/g, '<br>')}</div>`;

        // If AI recommends a product, append the product card format
        if (sender === 'ai' && product) {
            htmlContent += `
                <div class="product-card">
                    <h4>${product.name || 'Product'}</h4>
                    <ul>
                        <li><strong>Category:</strong> ${product.category || '-'}</li>
                        <li><strong>Color:</strong> ${product.color || '-'}</li>
                        <li><strong>Size:</strong> ${product.size || '-'}</li>
                    </ul>
                    <div class="product-price">$${product.price || 0}</div>
                    <div class="buy-instruction">
                        Agar sotib olishni istasangiz: "olaman", "ha", "sotib olaman", "olib ber" deb yozing
                    </div>
                </div>
            `;
        } else if (sender === 'ai' && !product && text.toLowerCase().includes('sotib olishni istasangiz')) {
             // Fallback if backend just sends text but it's a recommendation
             htmlContent += `
                <div class="buy-instruction mt-4">
                    Agar sotib olishni istasangiz:<br>
                    olaman<br>
                    ha<br>
                    sotib olaman<br>
                    olib ber
                </div>
             `;
        }

        msgDiv.innerHTML = htmlContent;
        chatBox.appendChild(msgDiv);
        scrollToBottom();
    }

    function appendTypingIndicator() {
        const id = 'typing-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.id = id;
        msgDiv.className = 'chat-message message-ai';
        msgDiv.innerHTML = '<span style="opacity: 0.6;">Yozmoqda...</span>';
        chatBox.appendChild(msgDiv);
        scrollToBottom();
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
