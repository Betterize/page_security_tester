import { defineConfig } from "astro-imagetools/config";

export default defineConfig({
    // placeholder
    // Jeśli nie jest ustawiony, to na raz wyswietla sie zarówno placeholder jak i zwykły obrazek
    // W przypadku elementów BackgroundImage, jeżeli nie jest ustawiony, to w konsoli są komunikaty, że serwer nie znalazł
    // zasobu https://betterize.pl/null.
    // Trzeba go ustawić na jedną z wartości: "blurred" | "tracedSVG" | "dominantColor"
    // Patrz: node_modules/astro-imagetools/api/utils/getFallbackImage.js
    // W pliku: index.astro, gdzie jest używany element BackgroundImage użyłem: "blurred"
    placeholder: "none",

    format: ["webp"],
    loading: "lazy",
    // layout: "fill",
    formatOptions: {
        jpg: {
            quality: 80,
        },
        png: {
            quality: 80,
        },
        webp: {
            quality: 80,
        },
    },
});
