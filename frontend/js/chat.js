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
            chatBox.innerHTML = `<div class="chat-message message-ai">Salom! Sizga qanday yordam bera olaman? Qanday kiyim qidiryapsiz?</div>`;
            localStorage.removeItem(storageKey);
        });
    }

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
                appendAIMessage('Xatolik yuz berdi: ' + error.message, null);
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
        msgDiv.innerHTML = `<div>${text.replace(/\n/g, '<br>')}</div>`;
        wrapper.appendChild(msgDiv);

        // Mahsulotlar kartochkasi
        if (products && products.length > 0) {
            const cardsContainer = document.createElement('div');
            cardsContainer.className = 'products-grid';

            products.forEach((p, index) => {
                const card = document.createElement('div');
                card.className = 'product-card-chat';
                card.innerHTML = `
                    <div class="product-card-header">
                        <span class="product-number">#${index + 1}</span>
                        <span class="product-category-badge">${p.category || ''}</span>
                    </div>
                    <h4 class="product-card-name">${p.name || 'Mahsulot'}</h4>
                    <div class="product-card-details">
                        <div class="detail-row"><span class="detail-label">Mavsum</span><span class="detail-value">${p.season || '-'}</span></div>
                        <div class="detail-row"><span class="detail-label">Rangi</span><span class="detail-value">${p.color || '-'}</span></div>
                        <div class="detail-row"><span class="detail-label">O'lchami</span><span class="detail-value">${p.size || '-'}</span></div>
                        <div class="detail-row price-row"><span class="detail-label">Narxi</span><span class="detail-value price-value">${Number(p.price).toLocaleString()} so'm</span></div>
                    </div>
                    <button class="buy-btn" data-product-id="${p.id}" data-product-name="${p.name}">Sotib olaman</button>
                `;

                // Sotib olish tugmasi - to'g'ridan-to'g'ri shu mahsulot ID si bilan
                card.querySelector('.buy-btn').addEventListener('click', async function() {
                    const btn = this;
                    const productId = btn.getAttribute('data-product-id');
                    const pName = btn.getAttribute('data-product-name');
                    btn.disabled = true;
                    btn.textContent = 'Kutilmoqda...';
                    try {
                        const res = await window.api.fetch(`/products/${productId}/buy`, {
                            method: 'POST'
                        });
                        btn.textContent = '✓ Sotib olindi!';
                        btn.style.background = 'linear-gradient(90deg,#22c55e,#16a34a)';
                        appendAIMessage(`✅ ${pName} muvaffaqiyatli sotib olindi! 🎉`, null);
                    } catch (err) {
                        btn.disabled = false;
                        btn.textContent = 'Sotib olaman';
                        appendAIMessage('❌ Xatolik: ' + err.message, null);
                    }
                });

                cardsContainer.appendChild(card);
            });

            wrapper.appendChild(cardsContainer);

            // Hint xabar
            const hint = document.createElement('div');
            hint.className = 'chat-message message-ai';
            hint.innerHTML = `<div style="font-size:0.82rem;opacity:0.7;">💡 Mahsulotni xohlasangiz tugmani bosing yoki "olaman", "maqul", "sotib olaman" deb yozing.</div>`;
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
        div.innerHTML = '<span style="opacity:0.6;">Yozmoqda...</span>';
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
        return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
});
