import { strapiApiBaseUrl } from "./consts";

export async function sendContactRequest(
    form: HTMLFormElement,
    onSuccess: Function,
    onErrror: Function
) {
    const formFields = {
        name: form.elements.namedItem("name"),
        email: form.elements.namedItem("email"),
        message: form.elements.namedItem("message"),
    };

    if (formFields.name.value == "") {
        onErrror(`Pole ${formFields.name.ariaLabel}' nie może być puste !`);
        return;
    }

    if (formFields.email.value == "") {
        onErrror(`Pole '${formFields.email.ariaLabel}' nie może być puste !`);
        return;
    }

    if (formFields.message.value == "") {
        onErrror(
            `Pole '${formFields.message.ariaLabel}' nie może być puste !`
        );
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
            onErrror(error);
        });
}
