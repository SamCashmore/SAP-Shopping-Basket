// Updating modal quantity value on 'Add to Basket' button click

var quantityOfItems

function updateModalQuantity() {
    quantityOfItems = document.getElementById("quantity").value
    document.getElementById("modalItemQuantity").innerText = quantityOfItems
    document.getElementById("formQuantity").value = quantityOfItems
    console.log(document.getElementById("formQuantity").value)
}

function submitCommand() {
    console.log(document.getElementById("formQuantity").value)
    console.log(document.getElementById("formProductId").value)
    console.log(document.getElementById("formPostcode").value)
}