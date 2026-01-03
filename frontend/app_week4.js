const ws = new WebSocket("ws://127.0.0.1:8000/ws");
let lastPrices = {};

ws.onopen = () => console.log("Connected to server");
ws.onerror = (err) => console.error("WebSocket error:", err);
ws.onclose = () => console.log("WebSocket closed");

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    document.getElementById("time").innerText = "Last Updated: " + data.time;

    let html = "";
    for (let stock in data.stocks) {
        const price = parseFloat(data.stocks[stock].toFixed(2));
        let cls = "";
        let arrow = "";
        if (lastPrices[stock] !== undefined) {
            if (price > lastPrices[stock]) { cls = "up"; arrow = " ↑"; }
            else if (price < lastPrices[stock]) { cls = "down"; arrow = " ↓"; }
        }
        lastPrices[stock] = price;
        html += `<div class="stock"><span>${stock}</span><span class="${cls}">$${price}${arrow}</span></div>`;
    }
    document.getElementById("stocks").innerHTML = html;
};
