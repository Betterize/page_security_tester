import { strapiApiBaseUrl } from "./consts";

export async function sendScanRequest(
    form: HTMLFormElement,
    onSuccess: Function,
    onError: Function
) {
    onSuccess();
    return;

    const formFields = {
        name: form.elements.namedItem("name"),
        email: form.elements.namedItem("email"),
        message: form.elements.namedItem("message"),
    };

    if (formFields.name.value == "") {
        onError(`Pole ${formFields.name.ariaLabel}' nie może być puste !`);
        return;
    }

    if (formFields.email.value == "") {
        onError(`Pole '${formFields.email.ariaLabel}' nie może być puste !`);
        return;
    }

    if (formFields.message.value == "") {
        onError(`Pole '${formFields.message.ariaLabel}' nie może być puste !`);
        return;
    }

    const params = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${import.meta.env.PUBLIC_STRAPI_TOKEN}`,
        },
        body: JSON.stringify({
            data: {
                name: formFields.name.value,
                email: formFields.email.value,
                message: formFields.message.value,
            },
        }),
    };

    await fetch(strapiApiBaseUrl + "/contact-forms", params)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then((data) => {
            // console.log("Form submitted successfully!", data);
            // Do something with the response data, if needed
            onSuccess();
        })
        .catch((error) => {
            // console.error("Error submitting form:", error);
            // Handle any errors that occur during the submission
            onError(error);
            // It seems that the scanner is not available at the moment. Please try again later or contact us via the contact form.
        });
}

export async function sendCodeVerificationRequest(
    form: HTMLFormElement,
    onSuccess: Function,
    onError: Function
) {
    onError("test");
    return;
}
