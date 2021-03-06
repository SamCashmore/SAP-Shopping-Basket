// Updating modal quantity value on 'Add to Basket' button click

var quantityOfItems

function updateModalQuantity() {
    quantityOfItems = document.getElementById("quantity").value
    document.getElementById("modalItemQuantity").innerText = quantityOfItems
    document.getElementById("formQuantity").value = quantityOfItems
}

function validPostcode(postcode) {
    // Regex pulled from internet somewhere, not sure if perfectly correct but seems to work fairly well
    var regex = /^(([A-Z][0-9]{1,2})|(([A-Z][A-HJ-Y][0-9]{1,2})|(([A-Z][0-9][A-Z])|([A-Z][A-HJ-Y][0-9]?[A-Z])))) [0-9][A-Z]{2}$/i;
    return regex.test(postcode);
}

function validateForm() {
    // Function to validate form, currently postcode
    var postcode = document.forms["postcodeForm"]["formPostcode"].value;
    if (postcode == "") {
        alert("Please enter a postcode");
        return false;
    } else if (!validPostcode(postcode)) {
        alert("Please enter a valid postcode");
        return false;
    }
}