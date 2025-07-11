document.addEventListener('DOMContentLoaded', () => {
    // --- Password Toggle Functionality ---
    // This function can be reused for any password field with a toggle icon
    const setupPasswordToggle = (toggleId, passwordInputId) => {
        const togglePassword = document.getElementById(toggleId);
        const passwordInput = document.getElementById(passwordInputId);

        if (togglePassword && passwordInput) {
            togglePassword.addEventListener('click', () => {
                // Toggle the type attribute
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);

                // Toggle the eye icon
                togglePassword.classList.toggle('fa-eye');
                togglePassword.classList.toggle('fa-eye-slash');
            });
        }
    };

    // Setup toggles for Login page
    setupPasswordToggle('togglePassword', 'password');

    // Setup toggles for Register page
    setupPasswordToggle('togglePasswordRegister', 'password');
    setupPasswordToggle('toggleConfirmPassword', 'confirmPassword');


    // --- Login Form Submission ---
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;
            if (!username || !password) {
                alert('Please enter both username and password.');
                return;
            }
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password }),
                });
                const data = await response.json();
                if (response.ok) {
                    // Login successful
                    localStorage.setItem('user_profile', JSON.stringify({ username: data.username }));
                    window.location.href = 'predict.html';
                } else {
                    alert(data.message || 'Invalid email or password. Please try again.');
                }
            } catch (error) {
                alert('An error occurred during login. Please try again later.');
            }
        });
    }

    // --- Register Form Submission ---
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            if (!username || !password || !confirmPassword) {
                alert('Please fill in all required fields.');
                return;
            }
            if (password !== confirmPassword) {
                alert('Passwords do not match.');
                return;
            }
            if (password.length < 6) {
                alert('Password must be at least 6 characters long.');
                return;
            }
            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password }),
                });
                const data = await response.json();
                if (response.ok) {
                    alert('Account created successfully! Please log in.');
                    window.location.href = 'login.html';
                } else {
                    alert(data.message || 'Registration failed. Please try again with different details.');
                }
            } catch (error) {
                alert('An error occurred during registration. Please try again later.');
            }
        });
    }
});

// Helper function for displaying messages (replace alert with custom modal in production)
function showMessage(message, type = 'info') {
    // In a real application, you'd implement a custom modal or toast notification here.
    // For now, we'll use alert for simplicity as per instructions.
    alert(message);
}
