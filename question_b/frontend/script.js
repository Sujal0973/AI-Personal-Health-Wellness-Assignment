const API_BASE_URL = "http://127.0.0.1:8000";

const form = document.getElementById("riskForm");
const predictButton = document.getElementById("predictButton");
const buttonText = document.getElementById("buttonText");
const buttonLoader = document.getElementById("buttonLoader");

const result = document.getElementById("result");
const apiError = document.getElementById("apiError");
const apiErrorText = document.getElementById("apiErrorText");

const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");

const newAssessment = document.getElementById("newAssessment");


function getNumber(id) {
    const value = document.getElementById(id).value;

    if (value === "") {
        return null;
    }

    return Number(value);
}


function getBinary(id) {
    return document.getElementById(id).checked ? 1 : 0;
}


function clearErrors() {
    document.querySelectorAll(".error").forEach((element) => {
        element.textContent = "";
    });
}


function showFieldError(field, message) {
    const error = document.getElementById(`${field}Error`);

    if (error) {
        error.textContent = message;
    }
}


function validateInput(data) {
    clearErrors();

    let valid = true;

    if (
        data.age === null ||
        !Number.isFinite(data.age) ||
        data.age < 1 ||
        data.age > 120
    ) {
        showFieldError("age", "Enter an age between 1 and 120.");
        valid = false;
    }

    if (data.sex === null || ![0, 1].includes(data.sex)) {
        showFieldError("sex", "Please select a sex.");
        valid = false;
    }

    if (
        data.ejection_fraction === null ||
        !Number.isFinite(data.ejection_fraction) ||
        data.ejection_fraction < 0 ||
        data.ejection_fraction > 100
    ) {
        showFieldError(
            "ejection_fraction",
            "Enter a value between 0 and 100."
        );
        valid = false;
    }

    if (
        data.serum_creatinine === null ||
        !Number.isFinite(data.serum_creatinine) ||
        data.serum_creatinine <= 0
    ) {
        showFieldError(
            "serum_creatinine",
            "Enter a value greater than 0."
        );
        valid = false;
    }

    if (
        data.serum_sodium === null ||
        !Number.isFinite(data.serum_sodium) ||
        data.serum_sodium < 0
    ) {
        showFieldError(
            "serum_sodium",
            "Enter a non-negative value."
        );
        valid = false;
    }

    if (
        data.platelets === null ||
        !Number.isFinite(data.platelets) ||
        data.platelets < 0
    ) {
        showFieldError(
            "platelets",
            "Enter a non-negative value."
        );
        valid = false;
    }

    if (
        data.creatinine_phosphokinase === null ||
        !Number.isFinite(data.creatinine_phosphokinase) ||
        data.creatinine_phosphokinase < 0
    ) {
        showFieldError(
            "creatinine_phosphokinase",
            "Enter a non-negative value."
        );
        valid = false;
    }

    return valid;
}


function setLoading(isLoading) {
    predictButton.disabled = isLoading;

    if (isLoading) {
        buttonText.classList.add("hidden");
        buttonLoader.classList.remove("hidden");
    } else {
        buttonText.classList.remove("hidden");
        buttonLoader.classList.add("hidden");
    }
}


function showResult(data) {
    const percentage = data.predicted_risk * 100;

    const riskLabel = document.getElementById("riskLabel");
    const riskIcon = document.getElementById("riskIcon");
    const riskBar = document.getElementById("riskBar");

    riskLabel.textContent = data.risk_label;

    document.getElementById("riskPercentage").textContent =
        percentage.toFixed(1);

    riskBar.style.width = `${percentage}%`;

    document.getElementById("thresholdValue").textContent =
        Number(data.threshold).toFixed(2);

    if (data.prediction === 1) {
        riskIcon.textContent = "!";
        riskIcon.style.background = "#fee2e2";
        riskIcon.style.color = "#dc2626";

        riskBar.style.background = "#dc2626";
        riskLabel.style.color = "#dc2626";
    } else {
        riskIcon.textContent = "✓";
        riskIcon.style.background = "#ecfdf5";
        riskIcon.style.color = "#15803d";

        riskBar.style.background = "#15803d";
        riskLabel.style.color = "#15803d";
    }

    result.classList.remove("hidden");

    result.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


function showError(message) {
    apiErrorText.textContent = message;

    apiError.classList.remove("hidden");

    apiError.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


async function checkApiHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);

        if (!response.ok) {
            throw new Error("API unavailable");
        }

        const data = await response.json();

        if (data.status === "healthy") {
            statusDot.classList.remove("offline");
            statusDot.classList.add("online");
            statusText.textContent = "API Online";
        } else {
            throw new Error("API unhealthy");
        }

    } catch (error) {
        statusDot.classList.remove("online");
        statusDot.classList.add("offline");
        statusText.textContent = "API Offline";
    }
}


form.addEventListener("submit", async (event) => {

    event.preventDefault();

    result.classList.add("hidden");
    apiError.classList.add("hidden");

    const data = {
        age: getNumber("age"),
        anaemia: getBinary("anaemia"),
        creatinine_phosphokinase:
            getNumber("creatinine_phosphokinase"),
        diabetes: getBinary("diabetes"),
        ejection_fraction:
            getNumber("ejection_fraction"),
        high_blood_pressure:
            getBinary("high_blood_pressure"),
        platelets: getNumber("platelets"),
        serum_creatinine:
            getNumber("serum_creatinine"),
        serum_sodium:
            getNumber("serum_sodium"),
        sex: getNumber("sex"),
        smoking: getBinary("smoking")
    };


    if (!validateInput(data)) {
        return;
    }


    setLoading(true);

    try {

        const response = await fetch(
            `${API_BASE_URL}/predict`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );


        const responseData = await response.json();


        if (!response.ok) {

            if (response.status === 422) {
                throw new Error(
                    "The submitted information failed server-side validation."
                );
            }

            throw new Error(
                "The prediction service could not process the request."
            );
        }


        showResult(responseData);


    } catch (error) {

        showError(
            error.message ||
            "Unable to connect to the prediction service."
        );

    } finally {

        setLoading(false);
    }
});


newAssessment.addEventListener("click", () => {

    form.reset();

    result.classList.add("hidden");
    apiError.classList.add("hidden");

    clearErrors();

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});


checkApiHealth();