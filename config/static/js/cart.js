const updateOrderQuantityForms = document.getElementsByClassName("update-order-quantity-form");

for (form of updateOrderQuantityForms) {
    form.children[1].addEventListener("click", function (e) {
        e.preventDefault();

        this.nextElementSibling.value = parseInt(this.nextElementSibling.value) + 1;

        this.parentElement.submit();
    });

    form.children[3].addEventListener("click", function (e) {
        e.preventDefault();
        if (this.previousElementSibling.value > 0) {
            this.previousElementSibling.value = parseInt(this.previousElementSibling.value) - 1;
            this.parentElement.submit();
        }
    });
}

const cartCheckbox = document.getElementsByClassName("checkbox");

cartCheckbox[0].addEventListener("click", function (e) {
    for (let i = 1; i < cartCheckbox.length; i++) {
        cartCheckbox[i].checked = this.checked;
    }
});

for (let i = 1; i < cartCheckbox.length; i++) {
    cartCheckbox[i].addEventListener("click", function (e) {
        for (let i = 1; i < cartCheckbox.length; i++) {
            if (cartCheckbox[i].checked == false) {
                cartCheckbox[0].checked = false;
                return;
            }
            cartCheckbox[0].checked = true;
        }
    });
}

const checkoutBtn = document.getElementById("checkout-btn");

checkoutBtn.addEventListener("click", function (e) {
    e.preventDefault();
    cartCheckoutForm = document.getElementById("cart-checkout-section");
    for (let i = 1; cartCheckbox.length > i; i++) {
        if (cartCheckbox[i].checked == true) {
            let checkoutItem = document.createElement("input");
            checkoutItem.type = "hidden";
            checkoutItem.name = "checkout-item-ids";
            checkoutItem.value = cartCheckbox[i].value;
            cartCheckoutForm.appendChild(checkoutItem);
        }
    }
    cartCheckoutForm.submit();
});
