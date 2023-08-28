import { defineConfig } from "windicss/helpers";
// import colors from "windicss/colors";
import plugin from "windicss/plugin";
import filters from "windicss/filters";
import forms from "windicss/forms";

export default defineConfig({
    attributify: true,
    darkMode: "class", // or 'media'
    shortcuts: {
        "header-1":
            "text-3xl lg:text-5xl max-w-4xl font-black text-gray-100 mb-4 lg:mb-6 mx-auto uppercase",
        "header-2":
            "text-2xl lg:text-4xl font-bold text-gray-100 max-w-xl mb-4 lg:mb-6 tracking-normal",
        "header-3": "text-lg lg:text-xl font-bold text-gray-100 max-w-xl mb-2",
        "p-paragraph":
            "text-md lg:text-lg font-normal text-gray-300 max-w-xl pb-3 leading-relaxed mx-auto",
        "p-proof-paragraph":
            "text-sm lg:text-md font-normal text-gray-300 max-w-xl pb-3 leading-relaxed mx-auto px-2 ",
        "blog-header": "lg:text-3xl text-left font-medium mb-6",
        "ordinary-text": "text-sm lg:text-md text-gray-300 max-w-2xl mx-auto",
        "button-cta": "px-16 py-4",
        "landing-p": "text-md text-gray-300 max-w-2xl mb-2 max-w-xl",
        "fancy-shadow":
            "box-shadow: rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px;",
        "transition-smooth":
            "transition duration-200 hover:(transition duration-200)",
        "image-animation":
            "md:(transition duration-500 hover:(origin-bottom transform -translate-y-2 duration-500 ))",
        "main-content": "px-4 xl:px-0 max-w-screen lg:max-w-6xl mx-auto",
        "outlined-text":
            "text-stroke-width-2 text-stroke-sky-500/40 text-transparent bg-clip-text bg-gradient-to-br from-sky-500 via-indigo-500 to-teal-500 font-black",
        // ---------------------------------------------------------------------------------------------
        "blog-header-1":
            "max-w-4xl text-4xl font-black text-gray-100 mb-4 lg:text-5xl lg:mb-6 mx-auto uppercase",
        "blog-header-2":
            "max-w-xl mb-4 text-3xl font-bold tracking-normal text-gray-100 capitalize lg:text-4xl lg:mt-8",
        "blog-header-3":
            "text-lg lg:text-xl font-bold text-gray-100 max-w-xl mb-4 lg:mt-8",
        "blog-header-4":
            "text-md lg:text-lg font-bold text-gray-100 max-w-xl mb-2 lg:mt-4",
    },
    theme: {
        extend: {
            fontFamily: {
                font1: ["Raleway"],
            },
            screens: {
                sm: "480px",
                md: "768px",
                lg: "1024px",
                xl: "1280px",
                "2xl": "1600px",
            },
            colors: {
                primary: "#ffd700",
                secondary: "ffffff",
                sidecol1: "ffffff",
                sidecol2: "ffffff",
                background: "151317",
            },
            filter: {
                none: "none",
                grayscale: "grayscale(1)",
                invert: "invert(1)",
                sepia: "sepia(1)",
            },
            backdropFilter: {
                none: "none",
                blur: "blur(20px)",
            },
            animation: {
                spin: "spin 1s linear infinite",
                ping: "ping 1s cubic-bezier(0, 0, 0.2, 1) infinite",
                pulse: "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
                bounce: "bounce 1s infinite",
                shock: {
                    animation: "shock",
                    transformOrigin: "center bottom",
                },
                flash: "flash",
                bubble: "bubble infinite",
                "rubber-band": "rubberBand",
                "shake-x": "shakeX",
                // ...
            },
            keyframes: {
                wiggle: {
                    "0%, 100%": { transform: "rotate(-3deg)" },
                    "50%": { transform: "rotate(3deg)" },
                },
            },
        },
    },
    variants: {
        filter: ["responsive"],
        backdropFilter: ["responsive"],
    },
    plugins: [
        require("@windicss/plugin-question-mark"),
        require("windicss/plugin/filters"),
        require("windicss/plugin/forms"),
        // ...
    ],
    // purge: ["./src/**/*.html", "./src/**/*.css", "./src/**/*.js"],
});
