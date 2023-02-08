// Cart functions
const countPill = document.getElementById("count-pill");
const count = parseInt(countPill.children[0].textContent);

if (count > 0) {
    countPill.style.display = "flex";
} else {
    countPill.style.display = "none";
}

// menu functions
const userMenuBtn = document.getElementById("user-menu-btn");
const userMenu = document.getElementById("user-menu");

const hideMenu = function () {
    userMenu.style.display = "none";
    window.removeEventListener("click", hideMenu);
};

userMenuBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    if (userMenu.style.display == "none" || !userMenu.hasAttribute("style")) {
        userMenu.style.display = "block";
        window.addEventListener("click", hideMenu);
    } else {
        hideMenu();
    }
});
