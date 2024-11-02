document.addEventListener('DOMContentLoaded', () => {
    let currentStep = 0; // Current step index
    let steps = []; // Array to hold steps from backend

    // Function to run code and get steps
    async function runCode() {
        const code = document.getElementById('code').value;
        const response = await fetch('/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code })
        });
        
        const data = await response.json();

        // Check if there are steps returned
        if (data.steps) {
            steps = data.steps; 
            currentStep = 0; // Reset step index
            visualizeStep(); // Start visualizing the first step
        } else {
            console.error('No steps received:', data);
        }
    }

    // Function to visualize the current step
    function visualizeStep() {
        if (currentStep < steps.length) {
            const step = steps[currentStep];
            updateDisplay(step);
            currentStep++;
        } else {
            console.log("Execution finished.");
        }
    }

    // Function to update the UI with the current step's data
    function updateDisplay(step) {
        // Clear previous display
        const output = document.getElementById('output');
        output.innerHTML = '';

        // Show current line of code being executed
        const currentLine = document.createElement('div');
        currentLine.textContent = `Executing: ${step.code}`;
        output.appendChild(currentLine);

        // Display variable states
        const variables = document.createElement('div');
        variables.textContent = 'Variables: ' + JSON.stringify(step.variables);
        output.appendChild(variables);

        // Highlight current line
        highlightCurrentLine(step.lineNumber);
    }

    // Function to highlight the current line in the code editor
    function highlightCurrentLine(lineNumber) {
        const codeArea = document.getElementById('code');
        const lines = codeArea.value.split('\n');

        // Highlight the current line
        codeArea.value = lines.map((line, index) => {
            return index + 1 === lineNumber ? `>>> ${line}` : line; // Prefix with arrow
        }).join('\n');
    }

    // Button to step through the visualization
    function stepThrough() {
        visualizeStep();
    }

    // Attach event listeners
    document.getElementById('run-code').addEventListener('click', runCode);
    document.getElementById('next-step').addEventListener('click', stepThrough);
});
