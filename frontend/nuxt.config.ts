export default defineNuxtConfig({
    telemetry: false,
    modules: [
        "@nuxt/devtools",
        "@nuxtjs/turnstile",
        "nuxt-api-party",
        "nuxt-gtag",
        "@unocss/nuxt",
        "@vueuse/nuxt",
    ],
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
