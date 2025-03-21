let socket;
let typingTimer;
const doneTypingInterval = 1000;  // Time in ms (1 second)
let messageInput;  // Declare without initializing

require.config({
    paths: {
      vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.34.0/min/vs"
    }
  });

  let monacoEditor;
  require(["vs/editor/editor.main"], function () {
    // Create the Monaco editor instance
    monacoEditor = monaco.editor.create(document.getElementById("editor"), {
        value: '# Online Python Playground\n# Use the online IDE to write, edit & run your Python code\n# Create, edit & delete files online\nprint("Try programiz.pro")',
      language: "python",
      theme: "vs-dark",
      automaticLayout: true,
      fontSize: 14,
      minimap: { enabled: false },
    });
  });

  // Run button logic: use the "/ide/python" endpoint
  document.getElementById("btnRun").addEventListener("click", async () => {
    if (!monacoEditor) {
      document.getElementById("console").textContent = "Editor not loaded yet!";
      return;
    }
    
    // Get code from the editor
    const code = monacoEditor.getValue();
    
    // Send code to the FastAPI endpoint "/ide/python"
    try {
      const response = await fetch("/ide/python", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      
      if (!response.ok) {
        document.getElementById("console").textContent =
          `Error ${response.status}: ${response.statusText}`;
        return;
      }
      const data = await response.json();
      // Display output in the console area
      document.getElementById("console").textContent = data.output || "No output";
    } catch (error) {
      document.getElementById("console").textContent = "Error: " + error;
    }
  });


function connectWebSocket() {
    const sessionId = document.getElementById("sessionId").value;
    const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    const ws_route = `/ws/${sessionId}`
    socket = new WebSocket(`${ws_scheme}://${window.location.host}${ws_route}`);

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        // alert("WebSocket error:", error);
    };

    socket.onmessage = (event) => {
        messageInput.value = event.data; // Update the textarea with received data
    };
}

document.addEventListener("DOMContentLoaded", function () {
    messageInput = document.getElementById("editor");
    
    if (!messageInput) {
        console.error("Error: Could not find element with id 'messageInput'. Make sure the element exists in your HTML.");
        return;
    }
    
    messageInput.addEventListener("input", () => {
        clearTimeout(typingTimer);
        // typingTimer = setTimeout(doneTyping, doneTypingInterval);
        // alert(messageInput.getValue);

        if (socket && socket.readyState === WebSocket.OPEN) {
            const encoder = new TextEncoder();
            const encodedData = encoder.encode(messageInput.getValue);
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