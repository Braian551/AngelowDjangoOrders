const togglePassword = document.getElementById('togglePassword');

togglePassword?.addEventListener('click', function () {
    const passwordInput = document.getElementById('password');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        this.textContent = '🙈';
    } else {
        passwordInput.type = 'password';
        this.textContent = '👁️';
    }
});

setTimeout(function () {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        if (typeof bootstrap !== 'undefined') {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        } else {
            alert.remove();
        }
    });
}, 5000);