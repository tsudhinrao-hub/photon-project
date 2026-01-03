const ws = new WebSocket("ws://127.0.0.1:8000/ws");

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    document.getElementById("price").innerText =
        `${data.stock}: $${data.price}`;
};
