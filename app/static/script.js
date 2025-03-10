let socket;

function connectWebSocket() {
    const sessionId = document.getElementById("sessionId").value;
    const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    const ws_route = `/ws/${sessionId}`;
    console.log(`Connecting to WebSocket: ${ws_scheme}://${window.location.host}${ws_route}`); // Use console.log instead of alert
    if (socket) {
        socket.close(); // Close existing connection if any
    }
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

const messageInput = document.getElementById("messageInput");

messageInput.addEventListener("input", () => {
    if (socket && socket.readyState === WebSocket.OPEN) {
        const encoder = new TextEncoder();
        const encodedData = encoder.encode(messageInput.value);
        const textData = new TextDecoder().decode(encodedData); // Convert to string
        socket.send(textData);
    }
});

document.getElementById("sessionId").addEventListener("change", connectWebSocket);

document.addEventListener("DOMContentLoaded", function () {
    connectWebSocket();
});
