/* =====================================================
   DROPDOWN MENU
===================================================== */

const dropdown = document.querySelector(".dropdown");
const btn = document.querySelector(".dropdown-btn");

btn.addEventListener("click", () => {

    dropdown.classList.toggle("active");

});


// close dropdown if clicked outside

document.addEventListener("click", function (e) {

    if (!dropdown.contains(e.target)) {

        dropdown.classList.remove("active");

    }

});


/* =====================================================
   LOGIN / SIGNUP TOGGLE
===================================================== */

function showSignup() {

    document.getElementById("login").style.display = "none";
    document.getElementById("signup").style.display = "block";

    document.getElementById("signupTab").classList.add("active");
    document.getElementById("loginTab").classList.remove("active");

}

function showLogin() {

    document.getElementById("signup").style.display = "none";
    document.getElementById("login").style.display = "block";

    document.getElementById("loginTab").classList.add("active");
    document.getElementById("signupTab").classList.remove("active");

}


/* =====================================================
   ADD TO CART (AJAX)
===================================================== */

document.querySelectorAll(".cart-form").forEach(form => {

    form.addEventListener("submit", function (e) {

        e.preventDefault();

        let btn = form.querySelector(".buy-btn");
        let formData = new FormData(form);

        fetch("/add_to_cart", {

            method: "POST",
            body: formData

        });

        btn.innerHTML = "✔ Added";
        btn.style.background = "green";

        setTimeout(() => {

            btn.innerHTML = "Add to Cart";
            btn.style.background = "";

        }, 2000);

    });

});


/* =====================================================
   CARD SCROLL ANIMATION
===================================================== */

const cards = document.querySelectorAll(".design-card");

if (cards.length > 0) {

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("show");

            }

        });

    }, { threshold: 0.1 });

    cards.forEach(card => {

        card.classList.add("fade-in");
        observer.observe(card);

    });

}


/* =====================================================
   NAVBAR SHADOW ON SCROLL
===================================================== */

window.addEventListener("scroll", function () {

    const nav = document.querySelector(".navbar");

    if (!nav) return;

    if (window.scrollY > 50) {

        nav.style.boxShadow = "0 15px 35px rgba(0,0,0,0.08)";

    }
    else {

        nav.style.boxShadow = "0 10px 25px rgba(0,0,0,0.05)";

    }

});


/* =====================================================
   FAVORITE HEART BUTTON
===================================================== */

document.querySelectorAll(".fav-btn").forEach(btn => {

    btn.addEventListener("click", () => {

        if (btn.classList.contains("active")) {

            btn.classList.remove("active");
            btn.style.color = "#999";

        }
        else {

            btn.classList.add("active");
            btn.style.color = "red";

        }

    });

});


/* =====================================================
   SEARCH BAR ACTIVE EFFECT
===================================================== */

const searchBox = document.querySelector(".search-container");
const searchInput = document.querySelector(".search-container input");

if (searchInput) {

    searchInput.addEventListener("focus", () => {

        searchBox.classList.add("active");

    });

    searchInput.addEventListener("blur", () => {

        searchBox.classList.remove("active");

    });

}


/* =====================================================
   SMOOTH PAGE LOADING
===================================================== */

window.addEventListener("load", function () {

    document.body.style.opacity = "1";

});


// =========================
// FEATURES BAR OF BANNER
// =========================
const track = document.querySelector(".features-track");

track.innerHTML += track.innerHTML;




