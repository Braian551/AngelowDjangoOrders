/*
    JavaScript compartido para pantallas de autenticación.

    Se usa en:
    - login.html
    - register.html

    Principio DRY:
    En vez de tener una función para login y otra para registro,
    usamos una sola lógica basada en el atributo data-password-toggle.
*/

/*
    Busca todos los botones que tengan data-password-toggle.

    Ejemplos:
    <button data-password-toggle="password">Ver</button>
    <button data-password-toggle="id_password1">Ver</button>
    <button data-password-toggle="id_password2">Ver</button>
*/
const passwordToggleButtons = document.querySelectorAll('[data-password-toggle]');

passwordToggleButtons.forEach(function (button) {
    button.addEventListener('click', function () {
        const inputId = this.getAttribute('data-password-toggle');
        const passwordInput = document.getElementById(inputId);

        if (!passwordInput) {
            return;
        }

        const isPasswordHidden = passwordInput.type === 'password';

        passwordInput.type = isPasswordHidden ? 'text' : 'password';
        this.textContent = isPasswordHidden ? 'Ocultar' : 'Ver';
    });
});