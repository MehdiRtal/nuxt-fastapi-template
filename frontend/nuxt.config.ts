export default defineNuxtConfig({
    telemetry: false,
    modules: [
        "@nuxtjs/eslint-module",
        "@nuxt/devtools",
        "@nuxtjs/turnstile",
        "nuxt-api-party",
        "@vueuse/nuxt",
        "nuxt-lodash",
        "@nuxtseo/module",
        "@nuxt/ui",
        "nuxt-primevue",
    ],
    css: ["primevue/resources/themes/lara-light-teal/theme.css"],
    ui: {
        icons: ["mdi", "simple-icons"],
    },
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
