export default defineNuxtConfig({
    telemetry: false,
    modules: [
        "@nuxt/devtools",
        "@nuxt/image",
        "@nuxtjs/google-fonts",
        "@nuxtjs/turnstile",
        "@nuxtjs/tailwindcss",
        "nuxt-api-party",
        "nuxt-gtag",
        "nuxt-icon",
    ],
    googleFonts: {
        display: "swap",
        families: {
            Roboto: true,
        },
    },
    turnstile: {
        siteKey: process.env.TURNSTILE_SITE_KEY,
        secretKey: process.env.TURNSTILE_SECRET_KEY,
    },
    apiParty: {
        endpoints: {
            api: {
                url: process.env.API_URL!,
            },
        },
    },
    gtag: {
        id: process.env.GTAG_ID,
        loadingStrategy: "async",
    },
});
