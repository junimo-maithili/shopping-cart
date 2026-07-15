// Displaying current product's price on the screen
chrome.storage.local.get("price", ({ price }) => {
    document.getElementById("cost").textContent = price;
});
document.getElementById("cost").textContent = price;
