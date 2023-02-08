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

const cartCheckBox = document.getElementsByClassName("checkbox");

cartCheckBox[0].addEventListener("click", function (e) {
    for (let i = 1; i < cartCheckBox.length; i++) {
        cartCheckBox[i].checked = this.checked;
    }
});

for (let i = 1; i < cartCheckBox.length; i++) {
    cartCheckBox[i].addEventListener("click", function (e) {
        for (let i = 1; i < cartCheckBox.length; i++) {
            if (cartCheckBox[i].checked == false) {
                cartCheckBox[0].checked = false;
                return;
            }
            cartCheckBox[0].checked = true;
        }
    });
}
