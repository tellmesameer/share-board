let socket;
let typingTimer;
const doneTypingInterval = 1000;  // Time in ms (1 second)
let messageInput;  // Declare without initializing

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
        messageInput.value = event.data; // Update the textarea with received data
    };
}

document.addEventListener("DOMContentLoaded", function () {
    messageInput = document.getElementById("editor");

    alert(messageInput.value);  // Debugging
    
    if (!messageInput) {
        console.error("Error: Could not find element with id 'messageInput'. Make sure the element exists in your HTML.");
        return;
    }
    
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

    connectWebSocket();
});

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