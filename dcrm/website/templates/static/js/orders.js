/*
    JavaScript del módulo de pedidos.

    El total mostrado en pantalla es solo una vista previa:
    Django lo recalcula de forma autoritativa al guardar el pedido.
*/

document.addEventListener('DOMContentLoaded', () => {
    const totalPreview = document.getElementById('orderCalculatedTotal');
    const itemsList = document.querySelector('.order-items-list');
    const emptyItemTemplate = document.getElementById('emptyOrderItemTemplate');
    const totalFormsInput = document.querySelector('input[name="items-TOTAL_FORMS"]');

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
            if (item.classList.contains('is-removing')) {
                return;
            }

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

    const bindItemInputs = (item) => {
        item.querySelectorAll('input').forEach((input) => {
            input.addEventListener('input', calculateTotal);
            input.addEventListener('change', calculateTotal);
        });
    };

    const addOrderItem = () => {
        if (!itemsList || !emptyItemTemplate || !totalFormsInput) {
            return;
        }

        const formIndex = Number.parseInt(totalFormsInput.value, 10);
        const html = emptyItemTemplate.innerHTML.replaceAll('__prefix__', formIndex);
        const wrapper = document.createElement('div');
        wrapper.innerHTML = html.trim();
        const newItem = wrapper.firstElementChild;

        itemsList.appendChild(newItem);
        totalFormsInput.value = String(formIndex + 1);
        bindItemInputs(newItem);
        calculateTotal();
    };

    const removeOrderItem = (item) => {
        const deleteInput = item.querySelector('input[name$="-DELETE"]');

        if (deleteInput) {
            deleteInput.checked = true;
        }

        item.classList.add('is-removing');
        calculateTotal();
    };

    document.querySelectorAll('[data-order-item]').forEach((item) => {
        bindItemInputs(item);
    });

    document.addEventListener('click', (event) => {
        const addButton = event.target.closest('#addOrderItem');
        const removeButton = event.target.closest('.order-remove-item');

        if (addButton) {
            addOrderItem();
            return;
        }

        if (removeButton) {
            const item = removeButton.closest('[data-order-item]');

            if (item) {
                removeOrderItem(item);
            }
        }
    });

    calculateTotal();
});
