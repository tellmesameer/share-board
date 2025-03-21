let socket;
let typingTimer;
const doneTypingInterval = 1000;  // Time in ms (1 second)
const messageInput = document.getElementById("messageInput");

function connectWebSocket() {
    const sessionId = document.getElementById("sessionId").value;
    const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    const ws_route = `/ws/${sessionId}`
    socket = new WebSocket(`${ws_scheme}://${window.location.host}${ws_route}`);

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        alert("WebSocket error:", error);
    };

    socket.onmessage = (event) => {
        const messageInput = document.getElementById("messageInput");
        messageInput.value = event.data; // Update the textarea with received data
    };
}


messageInput.addEventListener("input", () => {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);

    if (socket && socket.readyState === WebSocket.OPEN) {
        const encoder = new TextEncoder();
        const encodedData = encoder.encode(messageInput.value);
        const textData = new TextDecoder().decode(encodedData); // Convert to string
        socket.send(textData);
    }
});

//user is "finished typing," do something
function doneTyping() {
    const sessionId = document.getElementById("sessionId").value;
    const message = document.getElementById("messageInput").value;

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

document.addEventListener("DOMContentLoaded", function () {
    connectWebSocket();
}
);

// document.getElementById("sessionId").addEventListener("change", connectWebSocket);

fetch("/ide/python", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({ code: "print('Hello from the IDE')" }),
});



require.config({
    paths: {
        vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.34.0/min/vs"
    }
});

let monacoEditor;

require(["vs/editor/editor.main"], function () {
    // Create the editor
    monacoEditor = monaco.editor.create(document.getElementById("editor"), {
        value: '# Type your Python code here...\nprint("Hello from Monaco!")',
        language: "python",
        theme: "vs-dark", // "vs" for light theme
        automaticLayout: true,
        fontSize: 14,
        minimap: {
            enabled: false,
        },
    });
}); 

//   ####################################