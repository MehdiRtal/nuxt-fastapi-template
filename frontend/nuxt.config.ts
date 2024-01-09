export default defineNuxtConfig({
    extends: ["@nuxt/ui-pro"],
    modules: [
        "@nuxtjs/eslint-module",
        "@nuxt/devtools",
        "@nuxtjs/turnstile",
        "nuxt-api-party",
        "@vueuse/nuxt",
        "nuxt-lodash",
        "@nuxtseo/module",
        "@nuxt/ui",
        "nuxt-security",
    ],
    telemetry: false,
    ui: {
        icons: ["mdi"],
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
