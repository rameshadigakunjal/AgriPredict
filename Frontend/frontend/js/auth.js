document.addEventListener('DOMContentLoaded', () => {
    console.log('Auth.js loaded and DOM ready');
    
    // Get form elements once
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const usernameField = document.getElementById('username');
    const passwordField = document.getElementById('password');
    
    console.log('Form elements check:');
    console.log('- loginForm:', loginForm ? 'Found' : 'Not found');
    console.log('- registerForm:', registerForm ? 'Found' : 'Not found');
    console.log('- usernameField:', usernameField ? 'Found' : 'Not found');
    console.log('- passwordField:', passwordField ? 'Found' : 'Not found');
    
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
    if (loginForm) {
        console.log('Login form found, adding event listener');
        
        // Add a test click handler to the submit button
        const submitButton = loginForm.querySelector('button[type="submit"]');
        if (submitButton) {
            console.log('Submit button found');
            submitButton.addEventListener('click', (e) => {
                console.log('Submit button clicked');
            });
        }
        
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            console.log('Login form submitted');
            
            const username = usernameField.value.trim();
            const password = passwordField.value;
            
            console.log('Login data:', { username, password: password ? '***' : '' });
            
            if (!username || !password) {
                alert('Please enter both username and password.');
                return;
            }
            
            // Show loading state
            const submitButton = loginForm.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Logging in...';
            submitButton.disabled = true;
            
            try {
                console.log('Sending login request...');
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password }),
                });
                
                console.log('Login response status:', response.status);
                const data = await response.json();
                console.log('Login response data:', data);
                
                if (response.ok) {
                    // Login successful
                    localStorage.setItem('user_profile', JSON.stringify({ username: data.username }));
                    console.log('Login successful, redirecting to predict.html');
                    
                    // Show success message and redirect immediately
                    submitButton.textContent = 'Login Successful! Redirecting...';
                    submitButton.style.backgroundColor = '#28a745';
                    
                    // Redirect after a brief delay
                    setTimeout(() => {
                        window.location.href = 'predict.html';
                    }, 500);
                } else {
                    // Reset button state
                    submitButton.textContent = originalText;
                    submitButton.disabled = false;
                    alert(data.message || 'Invalid username or password. Please try again.');
                }
            } catch (error) {
                console.error('Login error:', error);
                // Reset button state
                submitButton.textContent = originalText;
                submitButton.disabled = false;
                alert('An error occurred during login. Please try again later.');
            }
        });
    } else {
        console.log('Login form not found');
    }

    // --- Register Form Submission ---
    if (registerForm) {
        console.log('Register form found, adding event listener');
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            console.log('Register form submitted');
            
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            
            console.log('Form data:', { username, password: password ? '***' : '', confirmPassword: confirmPassword ? '***' : '' });
            
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
                console.log('Sending registration request...');
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password }),
                });
                
                console.log('Registration response status:', response.status);
                const data = await response.json();
                console.log('Registration response data:', data);
                
                if (response.ok) {
                    console.log('Registration successful, redirecting to login.html');
                    
                    // Show success message and redirect
                    const submitButton = registerForm.querySelector('button[type="submit"]');
                    if (submitButton) {
                        submitButton.textContent = 'Registration Successful! Redirecting...';
                        submitButton.disabled = true;
                        submitButton.style.backgroundColor = '#28a745';
                    }
                    
                    // Redirect after a brief delay
                    setTimeout(() => {
                        window.location.href = 'login.html';
                    }, 1000);
                } else {
                    alert(data.message || 'Registration failed. Please try again with different details.');
                }
            } catch (error) {
                console.error('Registration error:', error);
                alert('An error occurred during registration. Please try again later.');
            }
        });
    } else {
        console.log('Register form not found');
    }
    
    // --- Check if user is logged in ---
    const checkLoginStatus = async () => {
        try {
            const response = await fetch('/check_session');
            const data = await response.json();
            
            if (data.logged_in) {
                // Update navigation to show logout option
                updateNavForLoggedInUser(data.user_id);
            }
        } catch (error) {
            console.error('Error checking login status:', error);
        }
    };
    
    // --- Update navigation for logged in user ---
    const updateNavForLoggedInUser = (userId) => {
        const navMenu = document.querySelector('.nav-menu ul');
        if (navMenu) {
            // Hide Login/Register, show Logout/Profile
            const loginLink = navMenu.querySelector('a[href="login_new.html"]');
            const registerLink = navMenu.querySelector('a[href="register_new.html"]');
            const logoutLink = navMenu.querySelector('#logoutNav');
            const profileLink = navMenu.querySelector('#profileNav');
            if (loginLink) loginLink.style.display = 'none';
            if (registerLink) registerLink.style.display = 'none';
            if (logoutLink) logoutLink.classList.remove('hidden');
            if (profileLink) profileLink.classList.remove('hidden');
            if (logoutLink) {
                logoutLink.addEventListener('click', handleLogout);
            }
        }
    };

    const handleLogout = (e) => {
        e.preventDefault();
        fetch('/logout', { method: 'POST' })
            .then(() => {
                localStorage.removeItem('access_token');
                localStorage.removeItem('user_profile');
                window.location.href = 'index.html';
            });
    };

    // Check login status on page load
    checkLoginStatus();
});

// Helper function for displaying messages (replace alert with custom modal in production)
function showMessage(message, type = 'info') {
    // In a real application, you'd implement a custom modal or toast notification here.
    // For now, we'll use alert for simplicity as per instructions.
    alert(message);
}
