document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('register-form').addEventListener('submit', function (event) {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;

        if (password !== confirmPassword) {
            event.preventDefault(); // Prevent form submission
            const errorMessage = document.getElementById('error-message');
            errorMessage.style.display = 'block'; // Show error message
        }
    });
});