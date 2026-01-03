const ws = new WebSocket("ws://127.0.0.1:8000/ws");
let last = {};

ws.onopen = () => console.log("Connected to stock dashboard");
ws.onerror = (err) => console.error("WebSocket error:", err);
ws.onclose = () => console.log("WebSocket connection closed");

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    for (let s in data) {
        const div = document.getElementById(s);

        // Set initial class if first update
        if (!last[s]) {
            div.className = "stock";
        } else {
            div.className = data[s] > last[s] ? "stock up" : "stock down";
        }

        div.innerText = `${s}: $${data[s].toFixed(2)}`;
        last[s] = data[s];
    }
};
