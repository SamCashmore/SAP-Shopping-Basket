// Updating modal quantity value on 'Add to Basket' button click

var quantityOfItems

function updateModalQuantity() {
    quantityOfItems = document.getElementById("quantity").value
    document.getElementById("modalItemQuantity").innerText = quantityOfItems
    document.getElementById("formQuantity").value = quantityOfItems
    console.log(document.getElementById("formQuantity").value)
}