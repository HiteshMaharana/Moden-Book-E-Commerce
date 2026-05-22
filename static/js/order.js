let currentStep = 0;

function nextStep() {

    const steps = document.querySelectorAll(".step");
    const lines = document.querySelectorAll(".line");

    if (currentStep < steps.length) {

        steps[currentStep].classList.add("active");

        if (currentStep > 0) {
            lines[currentStep - 1].classList.add("active");
        }

        currentStep++;

    }

}