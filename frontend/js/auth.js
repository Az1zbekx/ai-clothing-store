// auth.js - Authentication, registration, and role management

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const logoutBtn = document.getElementById('logout-btn');

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
});

async function handleLogin(e) {
    e.preventDefault();

    const submitBtn = e.target.querySelector('button[type="submit"]');
    const errorContainer = document.getElementById('auth-error');

    const username = e.target.username.value;
    const password = e.target.password.value;

    try {
        submitBtn.disabled = true;
        submitBtn.innerText = 'Logging in...';

        if (errorContainer) {
            errorContainer.innerHTML = '';
        }

        const formData = new URLSearchParams();

        formData.append("username", username);
        formData.append("password", password);

        const response = await fetch(
            "http://127.0.0.1:8000/auth/login",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/x-www-form-urlencoded"
                },
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Login failed"
            );
        }

        localStorage.setItem(
            "token",
            data.access_token
        );

        const userResponse =
            await window.api.fetch("/me");

        localStorage.setItem(
            "user",
            JSON.stringify(userResponse)
        );

        redirectBasedOnRole(
            userResponse.role
        );

    } catch (error) {

        if (errorContainer) {
            window.api.showError(
                "auth-error",
                error.message
            );
        } else {
            alert(
                "Login failed: " +
                error.message
            );
        }

        submitBtn.disabled = false;
        submitBtn.innerText = "Login";
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const errorContainer = document.getElementById('auth-error');
    const username = e.target.username.value;
    const password = e.target.password.value;

    try {
        submitBtn.disabled = true;
        submitBtn.innerText = 'Registering...';
        if(errorContainer) errorContainer.innerHTML = '';

        await window.api.fetch('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });

        // Redirect to login after successful registration
        window.location.href = 'login.html';

    } catch (error) {
        if(errorContainer) {
            window.api.showError('auth-error', error.message);
        } else {
            alert('Registration failed: ' + error.message);
        }
        submitBtn.disabled = false;
        submitBtn.innerText = 'Register';
    }
}

function handleLogout(e) {
    e.preventDefault();
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

function redirectBasedOnRole(role) {

    switch (role) {

        case "boss":
            window.location.href =
                "boss-dashboard.html";
            break;

        case "admin":
            window.location.href =
                "admin.html";
            break;

        case "customer":
            window.location.href =
                "customer.html";
            break;

        default:
            window.location.href =
                "customer.html";
    }
}

// Export for checking auth state on protected pages
window.auth = {
    checkAuth: () => {
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = 'login.html';
            return null;
        }
        try {
            return JSON.parse(localStorage.getItem('user'));
        } catch(e) {
            return null;
        }
    },
    logout: handleLogout
};
