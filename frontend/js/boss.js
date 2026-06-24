// boss.js - Boss dashboard, analytics, and AI logic

document.addEventListener('DOMContentLoaded', () => {
    // Only proceed if authenticated and role is boss (though auth.js should ideally block this entirely)
    const user = window.auth.checkAuth();
    if (!user || user.role !== 'boss') {
        if (user) { // user exists but wrong role
             window.location.href = 'index.html'; 
        }
        return;
    }

    // --- Boss AI Chat Logic ---
    let isAITyping = false;
    window.addEventListener('beforeunload', (e) => {
        if (isAITyping) {
            e.preventDefault();
            e.returnValue = "Iltimos, AI javob berishini kuting! Sahifadan chiqsangiz javob yo'qoladi.";
        }
    });
    const chatForm = document.getElementById('boss-chat-form');
    const chatInput = document.getElementById('boss-chat-input');
    const chatBox = document.getElementById('boss-chat-box');
    const sendBtn = document.getElementById('boss-send-btn');
    const clearBtn = document.getElementById('boss-clear-chat-btn');

    const storageKey = `boss_chat_history_${user.username}`;
    const savedChat = localStorage.getItem(storageKey);
    if (savedChat && chatBox) {
        chatBox.innerHTML = savedChat;
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    if (clearBtn && chatBox) {
        clearBtn.addEventListener('click', () => {
            chatBox.innerHTML = `
            <div class="chat-message message-ai">
                Assalomu alaykum, Boss! Biznesingiz haqida qanday ma'lumot kerak?
            </div>`;
            localStorage.removeItem(storageKey);
        });
    }

    if (chatForm) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            appendMessage(message, 'user');
            chatInput.value = '';
            chatInput.disabled = true;
            sendBtn.disabled = true;

            const typingId = appendTypingIndicator();
            isAITyping = true;

            try {
                const response = await window.api.fetch('/boss/ai', {
                    method: 'POST',
                    body: JSON.stringify({ message })
                });

                removeTypingIndicator(typingId);
                
                let aiReply = response.reply || response.response || response.message || JSON.stringify(response);
                appendMessage(aiReply, 'ai');

            } catch (error) {
                removeTypingIndicator(typingId);
                appendMessage('Xatolik yuz berdi: ' + error.message, 'ai');
            } finally {
                isAITyping = false;
                chatInput.disabled = false;
                sendBtn.disabled = false;
                chatInput.focus();
            }
        });
    }

    function appendMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-message message-${sender}`;
        msgDiv.innerHTML = `<div>${text.replace(/\\n/g, '<br>')}</div>`;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        localStorage.setItem(storageKey, chatBox.innerHTML);
    }

    function appendTypingIndicator() {
        const id = 'typing-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.id = id;
        msgDiv.className = 'chat-message message-ai';
        msgDiv.innerHTML = '<span style="opacity: 0.6;">Tahlil qilinmoqda...</span>';
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }
});

// Expose dashboard loading functions
window.boss = {
    loadDashboard: async () => {
        const content = document.getElementById('dashboard-content');
        try {
            const data = await window.api.fetch('/boss/dashboard', { method: 'GET' });
            content.innerHTML = `
                <div class="stats-grid">
                    <div class="card stat-card">
                        <div class="stat-title">Total Users</div>
                        <div class="stat-value">${data.total_users || 0}</div>
                    </div>
                    <div class="card stat-card">
                        <div class="stat-title">Total Products</div>
                        <div class="stat-value">${data.total_products || 0}</div>
                    </div>
                    <div class="card stat-card">
                        <div class="stat-title">Total Sales</div>
                        <div class="stat-value">${data.total_sales || 0}</div>
                    </div>
                    <div class="card stat-card">
                        <div class="stat-title">Total Revenue</div>
                        <div class="stat-value">$${data.total_revenue || 0}</div>
                    </div>
                </div>
            `;
        } catch (error) {
            content.innerHTML = '';
            window.api.showError('dashboard-error', 'Failed to load dashboard: ' + error.message);
        }
    },

    loadAnalytics: async () => {
        const content = document.getElementById('analytics-content');
        try {
            const data = await window.api.fetch('/boss/analytics', { method: 'GET' });
            
            // Format Top Product
            let topProductHtml = '<span class="text-muted">N/A</span>';
            if (data.top_product) {
                topProductHtml = `<strong>${data.top_product.name || data.top_product}</strong>`;
            }

            // Format Low Stock
            let lowStockHtml = '<ul>';
            if (data.low_stock && data.low_stock.length > 0) {
                data.low_stock.forEach(p => {
                    lowStockHtml += `<li style="color: var(--danger)">${p.name || p} (Stock: ${p.stock || p.quantity || 'Low'})</li>`;
                });
            } else {
                lowStockHtml += '<li><span style="color: var(--success)">All products stocked</span></li>';
            }
            lowStockHtml += '</ul>';

            content.innerHTML = `
                <div class="stats-grid">
                    <div class="card stat-card">
                        <div class="stat-title">Total Sales</div>
                        <div class="stat-value">${data.total_sales || 0}</div>
                    </div>
                    <div class="card stat-card">
                        <div class="stat-title">Total Revenue</div>
                        <div class="stat-value" style="color: #34d399">$${data.total_revenue || 0}</div>
                    </div>
                </div>
                <div class="stats-grid mt-4">
                    <div class="card" style="flex: 1">
                        <h3>Top Product</h3>
                        <p class="mt-4" style="font-size: 1.2rem">${topProductHtml}</p>
                    </div>
                    <div class="card" style="flex: 1">
                        <h3>Low Stock Alerts</h3>
                        <div class="mt-4">${lowStockHtml}</div>
                    </div>
                </div>
            `;
        } catch (error) {
            content.innerHTML = '';
            window.api.showError('analytics-error', 'Failed to load analytics: ' + error.message);
        }
    }
};
