// Displaying current product's price on the screen
chrome.storage.local.get("price", ({ price }) => {
    document.getElementById("cost").textContent = price;
});


(async () => {
    
    // Get message about price
    const { budgetMessage, price } = await chrome.storage.local.get([
        "budgetMessage",
        "price"
    ]);

    document.getElementById("cost").textContent = price || "Open an Amazon product to see it's price!";
    document.getElementById("message").textContent = budgetMessage || "No message";

});