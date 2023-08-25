export default defineNuxtConfig({
    telemetry: false,
    modules: [
        "@nuxt/devtools",
        "@nuxtjs/turnstile",
        "nuxt-api-party",
        "@unocss/nuxt",
        "@vueuse/nuxt",
        "nuxt-lodash",
        "nuxt-seo-kit"
    ],
    runtimeConfig: {
        nitroPort: process.env.NITRO_PORT,
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
});
