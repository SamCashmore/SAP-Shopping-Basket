document.querySelector(".minus-btn").setAttribute("disabled", "disabled");
if (maxQuantity != null && maxQuantity <= 1) {
    document.querySelector(".plus-btn").setAttribute("disabled", "disabled");
    if (maxQuantity == 0) {
        document.querySelector(".cart-btn").setAttribute("disabled", "disabled");
    }
};

var valueCount

// Price calculation
function priceTotal() {
    var total = valueCount * unitPrice;
    document.getElementById("totalPrice").innerText = total
}

// Minus button
document.querySelector(".minus-btn").addEventListener("click", function() {
    valueCount = document.getElementById("quantity").value;
    valueCount--;
    document.getElementById("quantity").value = valueCount

    if (valueCount == 1) {
        document.querySelector(".minus-btn").setAttribute("disabled", "disabled")
    }  
    if (maxQuantity != null && valueCount < maxQuantity) {
        document.querySelector(".plus-btn").removeAttribute("disabled");
        document.querySelector(".plus-btn").classList.remove("disabled")
    }

    // Updating total price
    priceTotal()
})

// Plus button
document.querySelector(".plus-btn").addEventListener("click", function() {
    valueCount = document.getElementById("quantity").value;
    valueCount++;
    document.getElementById("quantity").value = valueCount

    if (valueCount > 1) {
        document.querySelector(".minus-btn").removeAttribute("disabled");
        document.querySelector(".minus-btn").classList.remove("disabled")
    }  
    if (maxQuantity != null && valueCount == maxQuantity) {
        document.querySelector(".plus-btn").setAttribute("disabled", "disabled")
    }

    // Updating total price
    priceTotal()
})