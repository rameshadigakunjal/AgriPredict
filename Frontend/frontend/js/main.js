document.addEventListener('DOMContentLoaded', () => {
    // This function will be executed once the DOM is fully loaded.

    // Get all navigation links
    const navLinks = document.querySelectorAll('.nav-link');

    // Add click event listener to each navigation link
    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            // Remove 'active' class from all links
            navLinks.forEach(item => item.classList.remove('active'));

            // Add 'active' class to the clicked link
            event.currentTarget.classList.add('active');

            // Optional: If you want smooth scrolling for internal links (e.g., #sections)
            // For this project, we are redirecting to different HTML pages,
            // so smooth scrolling for internal anchors might not be the primary use case.
            // However, if you add sections on a single page later, this would be useful.
            const href = event.currentTarget.getAttribute('href');
            if (href.startsWith('#')) {
                event.preventDefault(); // Prevent default jump
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Only attach Predict Now/Get Started button handler on index.html
    if (window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/')) {
        const predictButtons = document.querySelectorAll('.btn-primary, .btn-secondary');
        predictButtons.forEach(button => {
            button.addEventListener('click', (event) => {
                // Prevent default link behavior if it's a button
                event.preventDefault();
                // Redirect to the predict.html page
                window.location.href = 'predict.html';
            });
        });
    }

    // You can add more general JavaScript functionalities here that apply across multiple pages,
    // or specific ones for the index.html page.
});
