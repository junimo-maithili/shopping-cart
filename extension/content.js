// Getting the price of the product on the current screen
var price = document.querySelector('.a-price .a-offscreen')?.textContent;
chrome.storage.local.set({ price });