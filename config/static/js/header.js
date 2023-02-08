const countPill = document.getElementById("count-pill");

if (countPill.children[0].textContent == "0") {
    countPill.style.display = "none";
} else {
    countPill.style.display = "flex";
}
