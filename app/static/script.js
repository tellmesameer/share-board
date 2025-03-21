let socket;
let typingTimer;
const doneTypingInterval = 1000;  // Time in ms (1 second)
let messageInput;  // assigned later in DOMContentLoaded

require.config({
    paths: {
        vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.34.0/min/vs"
    }
});

let monacoEditor;

// Initialize DOM-dependent elements and listeners after DOM load
document.addEventListener("DOMContentLoaded", function () {
    messageInput = document.getElementById("messageInput");

    connectWebSocket();

    messageInput.addEventListener("input", () => {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(doneTyping, doneTypingInterval);

        if (socket && socket.readyState === WebSocket.OPEN) {
            const encoder = new TextEncoder();
            const encodedData = encoder.encode(messageInput.value);
            const textData = new TextDecoder().decode(encodedData);
            socket.send(textData);
        }
    });

    require(["vs/editor/editor.main"], function () {
        monacoEditor = monaco.editor.create(document.getElementById("editor"), {
            value: '# Online Python Playground \n# Use the online IDE to write, edit & run your Python code \n# Create, edit & delete files online\nprint("Try programiz.pro")',
            language: "python",
            theme: "vs-dark",
            automaticLayout: true,
            fontSize: 14,
            minimap: {
                enabled: false,
            },
        });
        window.monacoEditor = monacoEditor; // expose editor globally for run button logic
    });
});

function connectWebSocket() {
    const sessionId = document.getElementById("sessionId").value;
    const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    const ws_route = `/ws/${sessionId}`;
    socket = new WebSocket(`${ws_scheme}://${window.location.host}${ws_route}`);

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        alert("WebSocket error:", error);
    };

    socket.onmessage = (event) => {
        // Use global messageInput instead of re-querying the DOM
        messageInput.value = event.data;
    };
}

function doneTyping() {
    const sessionId = document.getElementById("sessionId").value;
    const message = messageInput.value;

    fetch(`/${sessionId}`, {  // Corrected URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `message=${message}`
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

fetch("/ide/python", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({ code: "print('Hello from the IDE')" }),
});