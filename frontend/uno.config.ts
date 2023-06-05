import {
    defineConfig,
    presetUno,
    presetAttributify,
    presetTagify,
    presetWebFonts,
} from "unocss";

export default defineConfig({
    presets: [
        presetWebFonts({
            provider: "google",
            fonts: {
                sans: "Roboto",
            },
        }),
        presetUno(),
        presetAttributify(),
        presetTagify(),
    ],
});
