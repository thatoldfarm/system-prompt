// Simulated JSON containing "live components"
const jsonData = {
    indexHtml: '<div id="dynamic-content">This is dynamically loaded content.</div>',
    someLogic: 'console.log("Executing some logic")',
    jsShell: 'function executeCommand(cmd) { console.log("Executing:", cmd); }'
};

// Function to inject HTML into the DOM
function injectHtml() {
    const contentDiv = document.getElementById('content');
    contentDiv.innerHTML = jsonData.indexHtml;
}

// Function to inject JavaScript logic
function injectJs() {
    eval(jsonData.someLogic);
    eval(jsonData.jsShell);
}

// Initialize after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    injectHtml();
    injectJs();
});
