let socket;

function connectWebSocket() {
    const sessionId = document.getElementById("sessionId").value;
    socket = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    socket.onmessage = (event) => {
        const messageInput = document.getElementById("messageInput");
        messageInput.value = event.data; // Update the textarea with received data
    };
}

const messageInput = document.getElementById("messageInput");

messageInput.addEventListener("input", () => {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(messageInput.value);
    }
});

document.addEventListener("DOMContentLoaded", function () {
    connectWebSocket(); 
}
);


// document.getElementById("sessionId").addEventListener("change", connectWebSocket);
