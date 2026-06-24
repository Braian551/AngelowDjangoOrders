/*
    Botón para mostrar u ocultar la contraseña.

    Busca el botón con id="togglePassword".
    Si existe, le agrega un evento click.
*/
const togglePasswordButton = document.getElementById('togglePassword');

if (togglePasswordButton) {
    togglePasswordButton.addEventListener('click', function () {
        const passwordInput = document.getElementById('password');

        // Si no existe el input de contraseña, detenemos la función.
        if (!passwordInput) {
            return;
        }

        // Verifica si actualmente el campo está oculto.
        const isPassword = passwordInput.type === 'password';

        // Cambia entre texto visible y contraseña oculta.
        passwordInput.type = isPassword ? 'text' : 'password';

        // Cambia el texto del botón.
        this.textContent = isPassword ? 'Ocultar' : 'Ver';
    });
}

/*
    Cierre automático de alertas.

    Después de 5 segundos, busca las alertas dentro de .app-messages
    y las cierra usando Bootstrap.
*/
setTimeout(function () {
    const alerts = document.querySelectorAll('.app-messages .alert');

    alerts.forEach(function (alert) {
        if (typeof bootstrap !== 'undefined') {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        } else {
            alert.remove();
        }
    });
}, 5000);