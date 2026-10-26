const imageInput = document.getElementById("imageInput");

const previewImage =
    document.getElementById("previewImage");

const predictButton =
    document.getElementById("predictButton");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");

const prediction =
    document.getElementById("prediction");

const confidence =
    document.getElementById("confidence");

const errorMessage =
    document.getElementById("error");


// ==========================================
// IMAGE PREVIEW
// ==========================================

imageInput.addEventListener("change", function () {

    const file = imageInput.files[0];

    if (!file) {
        return;
    }

    const imageURL =
        URL.createObjectURL(file);

    previewImage.src = imageURL;

    previewImage.style.display = "block";

    result.style.display = "none";

    errorMessage.textContent = "";

});


// ==========================================
// PREDICT IMAGE
// ==========================================

async function predictImage() {

    const file = imageInput.files[0];


    // Check image
    if (!file) {

        errorMessage.textContent =
            "Please select a fashion image first.";

        return;
    }


    // Create FormData
    const formData = new FormData();

    formData.append(
        "image",
        file
    );


    // Show loading
    loading.style.display = "block";

    result.style.display = "none";

    errorMessage.textContent = "";


    try {

        // Send image to Flask backend
        const response = await fetch(
            "http://127.0.0.1:5000/predict",
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        // Check backend error
        if (!response.ok) {

            throw new Error(
                data.error || "Prediction failed."
            );

        }


        // Display prediction
        prediction.textContent =
            data.prediction;


        // Display confidence
        confidence.textContent =
            data.confidence + "%";


        result.style.display =
            "block";


    }

    catch (error) {

        errorMessage.textContent =
            "Error: " + error.message;

    }

    finally {

        loading.style.display =
            "none";

    }

}