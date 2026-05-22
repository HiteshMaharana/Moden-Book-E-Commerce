function updateActive() {
    document.querySelectorAll(".page").forEach((p, i) => {
        p.classList.remove("active");
        if (i === index) {
            p.classList.add("active");
        }
    });
}

function nextSlide() {
    let slides = document.getElementById("slides");
    let total = slides.children.length;

    if (index < total - 1) {
        index++;
        slides.style.transform = "translateX(-" + index * 100 + "%)";
        updateActive();
    }
}

function prevSlide() {
    let slides = document.getElementById("slides");

    if (index > 0) {
        index--;
        slides.style.transform = "translateX(-" + index * 100 + "%)";
        updateActive();
    }
}