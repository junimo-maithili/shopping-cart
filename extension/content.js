console.log("content.js is running!");

// Getting the price of the product on the current screen
var price = document.querySelector('.a-price .a-offscreen')?.textContent;
chrome.storage.local.set({ price });

//POST request to send price to backend
const priceInfo = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ priceInfo: price })
};

async function sendPrice() {
    try {

    await fetch('http://127.0.0.1:5000/submitExtensionData', priceInfo)
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));

    } catch (error) {
        console.log(error)
    }
}

sendPrice();



async function getMessage() {
    try {
    alert("message is on it's way")

    const response = await fetch('http://127.0.0.1:5000/budgetAnalysis')
    const data = await response.json()
    console.log(data)
    alert(data.message)

    } catch (error) {
        console.log(error)
        alert("didn't work :(")
    }

}

getMessage()