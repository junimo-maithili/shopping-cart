async function awaitUUID() {
    // Return promise (which will be UUID)
    
    let { UUID } = await chrome.storage.local.get("UUID");
    
    if (!UUID) {
        UUID = crypto.randomUUID()
        chrome.storage.local.set({  UUID })
    }
        
    // Send post request for UUID
    const userInfo = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ UUID })
    };

    const response = await fetch('http://127.0.0.1:5000/submitUUID', userInfo)
    const data = await response.json();
    console.log(data);

}


// Observing for price updates
(async () => {
    await awaitUUID();
    const observer = new MutationObserver((_, observer) => {
        const price = document.querySelector(".a-price .a-offscreen")?.textContent;
        if (price) {
            chrome.storage.local.set({ price });
            observer.disconnect();
            runRoutes(price);
        }
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
})();


// Logic to only get the message if the price is received
async function runRoutes(priceVal) {
    const priceSent = await sendPrice(priceVal)
    if (priceSent && priceVal) {
        const message = await getMessage()
        alert(JSON.stringify(message));
        console.log(message)
    }
}


// Getting the price of the product on the current screen
var price = document.querySelector('.a-price .a-offscreen')?.textContent;
chrome.storage.local.set({ "price": price });


// POST request to send price of product to backend
async function sendPrice(priceVal) {
    if (!priceVal) return false

    try {
        const priceInfo = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ priceInfo: priceVal })
        };

        await fetch('http://127.0.0.1:5000/submitExtensionData', priceInfo)
            .then(response => response.json())
            .then(data => console.log('Success:', data))
            .catch(error => console.error('Error:', error));

            return true

    } catch (error) {
        console.log(error)
        return false
    }
}



// GET request to receive message about purchase from backend
async function getMessage() {
    try {
    const response = await fetch('http://127.0.0.1:5000/budgetAnalysis')
    return await response.json()

    } catch (error) {
        console.log(error)
        alert("didn't work :(")
        return null
    }

}