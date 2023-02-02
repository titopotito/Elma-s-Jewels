const submit_form = document.getElementById("submit-form");
const sort_option = document.getElementById("sort-option");
const filter_checkboxes = document.getElementsByClassName("filter-checkbox");

const append_to_form_and_submit = function () {
    for (checkbox of filter_checkboxes) {
        submit_form.appendChild(checkbox);
    }
    submit_form.appendChild(sort_option);
    submit_form.submit();
};

sort_option.addEventListener("change", append_to_form_and_submit);
for (checkbox of filter_checkboxes) {
    checkbox.addEventListener("change", append_to_form_and_submit);
}
