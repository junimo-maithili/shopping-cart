console.log("content.js is running!");

// Getting the price of the product on the current screen
var price = document.querySelector('.a-price .a-offscreen')?.textContent;
chrome.storage.local.set({ price });

alert("price received!")

//POST request to send price to backend
const priceInfo = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ priceInfo: price })
};

async function sendPrice() {
    try {
    alert("Price is now in a json file :D")

    await fetch('http://127.0.0.1:5000/submitExtensionData', priceInfo)
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));

    alert("running extension. POST REQUEST SENT")
    } catch (error) {
        console.log(error)
        alert("didn't work :(")
    }
}

sendPrice();