// chat.js - Customer chat logic

document.addEventListener('DOMContentLoaded', () => {
    const user = window.auth.checkAuth();
    if (!user) return;

    const chatForm = document.getElementById('chat-form');
    let isAITyping = false;
    window.addEventListener('beforeunload', (e) => {
        if (isAITyping) {
            e.preventDefault();
            e.returnValue = "Iltimos, AI javob berishini kuting!";
        }
    });

    const chatInput = document.getElementById('chat-input');
    const chatBox = document.getElementById('chat-box');
    const sendBtn = document.getElementById('send-btn');
    const clearBtn = document.getElementById('clear-chat-btn');

    const storageKey = `chat_history_${user.username}`;
    const savedChat = localStorage.getItem(storageKey);
    if (savedChat) {
        chatBox.innerHTML = savedChat;
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            chatBox.innerHTML = `<div class="chat-message message-ai"><div>Salom! Sizga qanday yordam bera olaman? Qanday kiyim qidiryapsiz? 👗</div></div>`;
            localStorage.removeItem(storageKey);
        });
    }

    // ============================================================
    // EVENT DELEGATION — buy tugmalari localStorage dan tiklanganida
    // ham ishlashi uchun chatBox ustida bir event listener qo'yamiz
    // ============================================================
    chatBox.addEventListener('click', async function(e) {
        const btn = e.target.closest('.buy-btn');
        if (!btn) return;

        // Tugma allaqachon ishlatilganmi?
        if (btn.disabled || btn.classList.contains('bought')) return;

        const productId = btn.getAttribute('data-product-id');
        const pName = btn.getAttribute('data-product-name');

        if (!productId) {
            appendAIMessage('❌ Mahsulot ID topilmadi.', null);
            return;
        }

        btn.disabled = true;
        btn.textContent = 'Kutilmoqda...';

        try {
            const res = await window.api.fetch(`/products/${productId}/buy`, {
                method: 'POST'
            });

            btn.textContent = '✓ Sotib olindi!';
            btn.classList.add('bought');
            btn.style.background = 'linear-gradient(90deg,#22c55e,#16a34a)';
            btn.style.cursor = 'default';

            appendAIMessage(`✅ **${pName}** muvaffaqiyatli sotib olindi! Yaxshi xarid! 🎉`, null);
        } catch (err) {
            btn.disabled = false;
            btn.textContent = 'Sotib olaman';
            appendAIMessage('❌ Xatolik: ' + err.message, null);
        }

        localStorage.setItem(storageKey, chatBox.innerHTML);
    });

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            appendUserMessage(message);
            chatInput.value = '';
            chatInput.disabled = true;
            sendBtn.disabled = true;

            const typingId = appendTypingIndicator();
            isAITyping = true;

            try {
                const response = await window.api.fetch('/chat', {
                    method: 'POST',
                    body: JSON.stringify({ message })
                });

                removeTypingIndicator(typingId);

                const aiText = response.response || response.reply || '';
                const products = response.recommended_products || null;

                appendAIMessage(aiText, products);

            } catch (error) {
                removeTypingIndicator(typingId);
                appendAIMessage('❌ Xatolik yuz berdi: ' + error.message, null);
            } finally {
                isAITyping = false;
                chatInput.disabled = false;
                sendBtn.disabled = false;
                chatInput.focus();
            }
        });
    }

    function appendUserMessage(text) {
        const div = document.createElement('div');
        div.className = 'chat-message message-user';
        div.innerHTML = `<div>${escapeHtml(text)}</div>`;
        chatBox.appendChild(div);
        scrollToBottom();
        localStorage.setItem(storageKey, chatBox.innerHTML);
    }

    function appendAIMessage(text, products) {
        const wrapper = document.createElement('div');

        // AI text xabari
        const msgDiv = document.createElement('div');
        msgDiv.className = 'chat-message message-ai';
        // **bold** formatini qo'llab-quvvatlash
        const formattedText = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');
        msgDiv.innerHTML = `<div>${formattedText}</div>`;
        wrapper.appendChild(msgDiv);

        // Mahsulotlar kartochkasi
        if (products && products.length > 0) {
            const cardsContainer = document.createElement('div');
            cardsContainer.className = 'products-grid';

            products.forEach((p, index) => {
                const card = document.createElement('div');
                card.className = 'product-card-chat';

                // data-product-id va data-product-name to'g'ri o'rnatiladi
                card.innerHTML = `
                    <div class="product-card-header">
                        <span class="product-number">#${index + 1}</span>
                        <span class="product-category-badge">${escapeHtml(p.category || '')}</span>
                    </div>
                    <h4 class="product-card-name">${escapeHtml(p.name || 'Mahsulot')}</h4>
                    <div class="product-card-details">
                        <div class="detail-row"><span class="detail-label">Mavsum</span><span class="detail-value">${escapeHtml(p.season || '-')}</span></div>
                        <div class="detail-row"><span class="detail-label">Rangi</span><span class="detail-value">${escapeHtml(p.color || '-')}</span></div>
                        <div class="detail-row"><span class="detail-label">O'lchami</span><span class="detail-value">${escapeHtml(p.size || '-')}</span></div>
                        <div class="detail-row price-row"><span class="detail-label">Narxi</span><span class="detail-value price-value">${Number(p.price).toLocaleString()} so'm</span></div>
                    </div>
                    <button
                        class="buy-btn"
                        data-product-id="${p.id}"
                        data-product-name="${escapeHtml(p.name || 'Mahsulot')}"
                    >Sotib olaman</button>
                `;

                cardsContainer.appendChild(card);
            });

            wrapper.appendChild(cardsContainer);

            // Hint xabar
            const hint = document.createElement('div');
            hint.className = 'chat-message message-ai';
            hint.innerHTML = `<div style="font-size:0.82rem;opacity:0.7;">💡 Kerakli mahsulot tugmasini bosing!</div>`;
            wrapper.appendChild(hint);
        }

        chatBox.appendChild(wrapper);
        scrollToBottom();
        localStorage.setItem(storageKey, chatBox.innerHTML);
    }

    function appendTypingIndicator() {
        const id = 'typing-' + Date.now();
        const div = document.createElement('div');
        div.id = id;
        div.className = 'chat-message message-ai';
        div.innerHTML = `<span style="opacity:0.6;">
            <span class="typing-dot">●</span>
            <span class="typing-dot">●</span>
            <span class="typing-dot">●</span>
        </span>`;
        chatBox.appendChild(div);
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

    function escapeHtml(text) {
        if (typeof text !== 'string') return String(text);
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});
