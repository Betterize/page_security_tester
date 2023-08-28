import { defineConfig } from "astro/config";
import { astroImageTools } from "astro-imagetools";
import windicss from "astro-windicss";
import critters from "astro-critters";
import partytown from "@astrojs/partytown";
import sitemap from "@astrojs/sitemap";
import compressor from "astro-compressor";

export default defineConfig({
    output: "static",
    site: "https://betterize.pl",
    integrations: [
        astroImageTools,
        windicss(),
        critters(),
        partytown({
            config: {
                forward: ["dataLayer.push"],
            },
        }),
        sitemap({
            filter: (page) =>
                page !== "https://security-scan.betterize.pl/test/" &&
                page !== "https://security-scan.betterize.pl/thank_you/" &&
                page !==
                    "https://security-scan.betterize.pl/pl/dziękujemy_za_kontakt/" &&
                page !== "https://security-scan.betterize.pl/~partytown/",
        }),
        compressor({
            gzip: false,
            brotli: true,
        }),
    ],
});
