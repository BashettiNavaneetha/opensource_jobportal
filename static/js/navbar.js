document.addEventListener("DOMContentLoaded", function () {
    let nav = document.querySelector("nav");

    window.addEventListener("scroll", function () {
        if (window.scrollY > 50) {
            nav.classList.add("scrolled");
        } else {
            nav.classList.remove("scrolled");
        }
    });

    // Mobile menu toggle (optional)
    let menuBtn = document.querySelector(".menu-btn");
    let navList = document.querySelector("nav ul");

    menuBtn.addEventListener("click", function () {
        navList.classList.toggle("show");
    });
});
