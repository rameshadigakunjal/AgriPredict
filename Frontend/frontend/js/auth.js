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
            event.preventDefault(); // Prevent default form submission

            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;

            // Basic client-side validation
            if (!username || !password) {
                alert('Please enter both username and password.');
                return;
            }

            try {
                // Replace with your actual Flask backend login endpoint
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
                    console.log('Login successful:', data);
                    // Save token if available
                    if (data.access_token) {
                        localStorage.setItem('access_token', data.access_token);
                    }
                    // Save user profile (username/email)
                    if (data.username) {
                        localStorage.setItem('user_profile', JSON.stringify({
                            username: data.username
                        }));
                    }
                    window.location.href = 'predict.html';
                } else {
                    // Login failed
                    console.error('Login failed:', data.message || 'Unknown error');
                    alert(data.message || 'Invalid email or password. Please try again.'); // Use a custom modal
                }
            } catch (error) {
                console.error('Network error or unexpected issue during login:', error);
                alert('An error occurred during login. Please try again later.'); // Use a custom modal
            }
        });
    }

    // --- Register Form Submission ---
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent default form submission

            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;

            // Basic client-side validation
            if (!username || !password || !confirmPassword) {
                alert('Please fill in all required fields.');
                return;
            }

            if (password !== confirmPassword) {
                alert('Passwords do not match.'); // Use a custom modal
                return;
            }

            if (password.length < 6) { // Example: minimum password length
                alert('Password must be at least 6 characters long.'); // Use a custom modal
                return;
            }

            try {
                // Replace with your actual Flask backend registration endpoint
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password
                    }),
                });

                const data = await response.json();

                if (response.ok) {
                    // Registration successful
                    console.log('Registration successful:', data);
                    alert('Account created successfully! Please log in.'); // Use a custom modal
                    window.location.href = 'login.html'; // Redirect to login page
                } else {
                    // Registration failed
                    console.error('Registration failed:', data.message || 'Unknown error');
                    alert(data.message || 'Registration failed. Please try again with different details.'); // Use a custom modal
                }
            } catch (error) {
                console.error('Network error or unexpected issue during registration:', error);
                alert('An error occurred during registration. Please try again later.'); // Use a custom modal
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
