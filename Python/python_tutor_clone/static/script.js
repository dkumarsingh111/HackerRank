let currentStep = 0;
let codeExecutionSteps = [];

// document.getElementById('run').addEventListener('click', () => {
//     const code = document.getElementById('code').value;
//     fetch('/execute', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ code })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.error) {
//             document.getElementById('output').textContent = 'Error: ' + data.error;
//         } else {
//             codeExecutionSteps = data.steps; // Store execution steps for stepping
//             currentStep = 0; // Reset current step
//             displayVariables(data);
//         }
//     });
// });

document.getElementById('run').addEventListener('click', () => {
    const code = document.getElementById('code').value;
    fetch('/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code })
    })
    .then(response => response.json())
    .then(data => {
        const outputElement = document.getElementById('output');
        if (data.success) {
            outputElement.textContent = data.output;
        } else {
            outputElement.textContent = 'Error: ' + data.error;
        }
    });
});

document.getElementById('step').addEventListener('click', () => {
    if (currentStep < codeExecutionSteps.length) {
        const step = codeExecutionSteps[currentStep++];
        displayVariables(step);
    }
});

function displayVariables(data) {
    const variablesDiv = document.getElementById('variables');
    variablesDiv.innerHTML = JSON.stringify(data, null, 2); // Display variables
}
