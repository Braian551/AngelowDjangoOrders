/*
    Cierre automático de mensajes globales de Django.

    Este archivo se carga desde base.html.
    Aplica para cualquier página que muestre mensajes:
    - login
    - registro
    - home
    - pedidos
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