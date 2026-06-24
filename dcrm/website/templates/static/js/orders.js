/*
    JavaScript del módulo de pedidos.

    El total mostrado en pantalla es solo una vista previa:
    Django lo recalcula de forma autoritativa al guardar el pedido.
*/

document.addEventListener('DOMContentLoaded', () => {
    const totalPreview = document.getElementById('orderCalculatedTotal');

    if (!totalPreview) {
        return;
    }

    const parseMoney = (value) => {
        const normalizedValue = String(value || '')
            .replace(/\./g, '')
            .replace(',', '.');

        return Number.parseFloat(normalizedValue) || 0;
    };

    const formatMoney = (value) => {
        return new Intl.NumberFormat('es-CO', {
            style: 'currency',
            currency: 'COP',
            minimumFractionDigits: 2,
        }).format(value);
    };

    const calculateTotal = () => {
        let total = 0;

        document.querySelectorAll('[data-order-item]').forEach((item) => {
            const deleteInput = item.querySelector('input[name$="-DELETE"]');

            if (deleteInput && deleteInput.checked) {
                return;
            }

            const quantityInput = item.querySelector('input[name$="-quantity"]');
            const unitPriceInput = item.querySelector('input[name$="-unit_price"]');
            const quantity = parseMoney(quantityInput?.value);
            const unitPrice = parseMoney(unitPriceInput?.value);

            total += quantity * unitPrice;
        });

        totalPreview.textContent = formatMoney(total);
    };

    document.querySelectorAll('[data-order-item] input').forEach((input) => {
        input.addEventListener('input', calculateTotal);
        input.addEventListener('change', calculateTotal);
    });

    calculateTotal();
});
