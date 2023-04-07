export default defineNuxtConfig({
    telemetry: false,
    modules: [
        "@nuxt/devtools",
        "@nuxtjs/google-fonts",
        "@nuxtjs/turnstile",
        "@unocss/nuxt",
        "nuxt-headlessui",
        "nuxt-api-party",
        "nuxt-gtag",
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
