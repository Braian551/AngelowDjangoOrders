/*
    Muestra u oculta la contraseña en la pantalla de login.

    El botón debe tener:
    id="togglePassword"

    El input debe tener:
    id="password"
*/

const togglePasswordButton = document.getElementById('togglePassword');

if (togglePasswordButton) {
    togglePasswordButton.addEventListener('click', function () {
        const passwordInput = document.getElementById('password');

        if (!passwordInput) {
            return;
        }

        const isPassword = passwordInput.type === 'password';

        passwordInput.type = isPassword ? 'text' : 'password';
        this.textContent = isPassword ? 'Ocultar' : 'Ver';
    });
}