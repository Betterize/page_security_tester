import { strapiApiBaseUrl } from "./consts";

export async function sendScanRequest(
    form: HTMLFormElement,
    onSuccess: Function,
    onError: Function
) {
    const formFields = {
        website: form.elements.namedItem("website") as HTMLFormElement,
        email: form.elements.namedItem("email") as HTMLFormElement,
        marketing: form.elements.namedItem("marketing") as HTMLFormElement,
        rodo: form.elements.namedItem("rodo") as HTMLFormElement,
        tool: form.elements.namedItem("tool") as HTMLFormElement,
    };

    if (formFields.website.value == "") {
        onError(`Field ${formFields.website.ariaLabel} can not be empty!`);
        return;
    }

    if (formFields.email.value == "") {
        onError(`Field ${formFields.email.ariaLabel} can not be empty!`);
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
                website: formFields.website.value,
                email: formFields.email.value,
                accepted_regulations: formFields.tool.checked,
                accepted_marketing: formFields.marketing.checked,
                personal_data_processing: formFields.rodo.checked,
            },
        }),
    };

    await fetch(strapiApiBaseUrl + "/page-security-tests", params)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok. Try again later");
            }
            return response.json();
        })
        .then((_) => {
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
    const formFields = {
        id: form.elements.namedItem("id") as HTMLFormElement,
        code: form.elements.namedItem("code") as HTMLFormElement,
    };

    if (formFields.id.value == "") {
        onError(`Field ${formFields.id.ariaLabel} can not be empty!`);
        return;
    }
    if (formFields.code.value == "") {
        onError(`Field ${formFields.code.ariaLabel} can not be empty!`);
        return;
    }

    const params = {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${import.meta.env.PUBLIC_STRAPI_TOKEN}`,
        },
        body: JSON.stringify({
            id: Number(formFields.id.value),
            code: formFields.code.value,
        }),
    };
    const response = await fetch(strapiApiBaseUrl + "/verify_code", params);
    if (!response.ok) {
        const body = await response.text();
        onError(body);
    } else {
        onSuccess();
    }
}
