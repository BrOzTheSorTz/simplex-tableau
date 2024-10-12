// Simplex Solver Logic
let contadorRestricciones = 0;
let contadorVariables = 2;
function agregarRestriccion() {
    event.preventDefault(); // Evita que el formulario se envíe
    // Clear the placeholder text if it's the first restriction
    if (contadorRestricciones === 0) {
        const texto = document.getElementById('texto_restricciones');
        texto.textContent = '';
    }
    contadorRestricciones++;
    const divRestricciones = document.getElementById('div-restricciones');

    const nuevaRestriccion = document.createElement('div');
    nuevaRestriccion.classList.add('restriccion');
    nuevaRestriccion.id = `restriccion-${contadorRestricciones}`;
    nuevaRestriccion.innerHTML = `
        <div class="mb-2">
            ${generarInputsRestriccion()}
            <span> &le; </span>
            <input type="text" name="termino_independiente[]" placeholder="Término independiente" class="termino-independiente">
            <button type="button" class="btn btn-danger btn-sm ml-2" onclick="eliminarRestriccion(${contadorRestricciones})">Eliminar</button>
        </div>
    `;
    divRestricciones.appendChild(nuevaRestriccion);
    updateSolveButton(); // Update the solve button state
}

function agregarVariable() {
    event.preventDefault(); // Evita que el formulario se envíe
    contadorVariables++;
    const divFuncion = document.getElementById('funcion-objetivo');
    const nuevasVariables = document.querySelectorAll('.restriccion');

    const nuevoInputFuncion = document.createElement('span');
    nuevoInputFuncion.innerHTML = `
        <span> + </span>
        <input type="text" name="coeficientes[]" placeholder="Coeficiente x${contadorVariables}" class="coef-input">
    `;
    divFuncion.appendChild(nuevoInputFuncion);

    nuevasVariables.forEach(function (restriccion) {
        const coeficientes = restriccion.querySelector('.coeficientes');
        const nuevoInputRestriccion = document.createElement('span');
        nuevoInputRestriccion.innerHTML = `
            <span> + </span>
            <input type="text" name="restriccion_coeficientes[]" placeholder="Coeficiente x${contadorVariables}" class="coef-input">
        `;
        coeficientes.appendChild(nuevoInputRestriccion);
    });
    updateSolveButton(); // Update the solve button state
}

function eliminarVariable() {
    event.preventDefault(); // Evita que el formulario se envíe
    if (contadorVariables > 2) {
        const divFuncion = document.getElementById('funcion-objetivo');
        divFuncion.lastChild.remove();
        contadorVariables--;

        const restricciones = document.querySelectorAll('.restriccion .coeficientes');
        restricciones.forEach(function (coef) {
            coef.lastChild.remove();
        });
        updateSolveButton(); // Update the solve button state
    }
}

function generarInputsRestriccion() {
    let inputs = `<div class="coeficientes d-inline-block">`;
    for (let i = 1; i <= contadorVariables; i++) {
        inputs += `
            <input type="text" name="restriccion_coeficientes[]" placeholder="Coeficiente x${i}" class="coef-input">
            ${i < contadorVariables ? '<span> + </span>' : ''}
        `;
    }
    inputs += `</div>`;
    return inputs;
}

function eliminarRestriccion(id) {
    const restriccion = document.getElementById(`restriccion-${id}`);
    restriccion.remove();
    --contadorRestricciones;
    if (contadorRestricciones === 0) {
        const texto = document.getElementById('texto_restricciones');
        texto.textContent = "¡ Añade alguna restricción para empezar !";
    }
    updateSolveButton(); // Update the solve button state
}

// Function to enable/disable the Solve button
function updateSolveButton() {
    const restrictions = document.querySelectorAll('.restriccion');
    const objectiveFunction = document.querySelectorAll('input[name="coeficientes[]"]');
    const solveButton = document.getElementById('solve-button');

    // Enable the solve button if there is at least one restriction and one coefficient
    if (restrictions.length > 0 && objectiveFunction.length > 0 && objectiveFunction[0].value.trim() !== "") {
        solveButton.disabled = false;
    } else {
        solveButton.disabled = true;
    }
}
document.addEventListener("DOMContentLoaded", function() {


    // Event listeners to dynamically check the objective function inputs
    document.addEventListener('input', (event) => {
        if (event.target.matches('input[name="coeficientes[]"]')) {
            updateSolveButton(); // Update button state when coefficients change
        }
    });



});
function submitForm() {
    const form = document.getElementById('simplex-form');
    const submitButton = document.getElementById('solve-button');

    // Crear una matriz vacía para los coeficientes
    const coeficientes = [0];
    const restricciones = [];

    // Obtener coeficientes de la función objetivo
    const coefInputs = form.querySelectorAll('input[name="coeficientes[]"]');
    coefInputs.forEach(input => {
        if (input.value) {
            coeficientes.push(parseFloat(input.value));
        }
    });

    // Obtener restricciones
    const restriccionesInputs = form.querySelectorAll('.restriccion');
    restriccionesInputs.forEach(restriccion => {
        const coef_restricciones = [];
        const limiteInput = restriccion.querySelector('input[name="termino_independiente[]"]');
        if (limiteInput.value) {
            coef_restricciones.push(parseFloat(limiteInput.value));
        }
        const coefInputs = restriccion.querySelectorAll('input[name="restriccion_coeficientes[]"]');
        coefInputs.forEach(input => {
            if (input.value) {
                coef_restricciones.push(parseFloat(input.value));
            }
        });
        restricciones.push(coef_restricciones);
    });

    // Crear la matriz
    const matriz = [coeficientes, restricciones];
    console.log('Matriz a enviar:', matriz); // Para depuración

    // Deshabilitar el botón para evitar envíos duplicados
    submitButton.disabled = true;

    // Enviar datos a Flask
    fetch('/solve', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(matriz),
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                console.error('Error response text:', text); // Log del texto de respuesta
                throw new Error(text); // Lanza un error con el texto
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Respuesta del servidor:', data);
        // Mostrar el resultado en el div 'result'
        div_resultado =document.getElementById('infor-result');
        div_resultado.textContent = JSON.stringify(data);
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('result').textContent = `Error: ${error.message}`;
    }).finally(() => {
        // Habilitar el botón nuevamente
        submitButton.disabled = false;
    });

    // Prevenir el envío del formulario
    return false;
}
