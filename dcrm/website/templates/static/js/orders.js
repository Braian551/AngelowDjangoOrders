/*
    JavaScript del módulo de pedidos.

    El total mostrado en pantalla es solo una vista previa:
    Django lo recalcula de forma autoritativa al guardar el pedido.
*/

document.addEventListener('DOMContentLoaded', () => {
    // Elementos principales conectados con order_form.html.
    const totalPreview = document.getElementById('orderCalculatedTotal');
    const itemsList = document.querySelector('.order-items-list');
    const emptyItemTemplate = document.getElementById('emptyOrderItemTemplate');
    const totalFormsInput = document.querySelector('input[name="items-TOTAL_FORMS"]');

    if (!totalPreview) {
        return;
    }

    // Convierte valores escritos por el usuario a número.
    // Acepta entradas con punto de miles o coma decimal para hacerlo más tolerante.
    const parseMoney = (value) => {
        const normalizedValue = String(value || '')
            .replace(/\./g, '')
            .replace(',', '.');

        return Number.parseFloat(normalizedValue) || 0;
    };

    // Presenta el total en formato de moneda colombiana.
    const formatMoney = (value) => {
        return new Intl.NumberFormat('es-CO', {
            style: 'currency',
            currency: 'COP',
            minimumFractionDigits: 2,
        }).format(value);
    };

    // Recalcula la vista previa del total recorriendo todos los ítems visibles.
    const calculateTotal = () => {
        let total = 0;

        document.querySelectorAll('[data-order-item]').forEach((item) => {
            // Las filas ocultas por eliminación visual no deben sumar al total.
            if (item.classList.contains('is-removing')) {
                return;
            }

            const deleteInput = item.querySelector('input[name$="-DELETE"]');

            // Django recibe DELETE en el POST; aquí también lo respetamos para la vista previa.
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

    // Enlaza eventos de una fila para que cualquier cambio actualice el total.
    const bindItemInputs = (item) => {
        item.querySelectorAll('input').forEach((input) => {
            input.addEventListener('input', calculateTotal);
            input.addEventListener('change', calculateTotal);
        });
    };

    // Agrega una fila nueva usando el empty_form de Django.
    // La clave es reemplazar __prefix__ por el índice real del formset.
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

    // Elimina visualmente una fila y marca DELETE cuando Django la necesita.
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

    // Delegación de eventos: funciona para botones existentes y también para filas nuevas.
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
