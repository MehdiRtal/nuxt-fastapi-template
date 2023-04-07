import {
    defineConfig,
    presetUno,
    presetIcons,
    presetWebFonts,
    presetAttributify,
    presetTagify,
} from "unocss";

export default defineConfig({
    presets: [
        presetUno(),
        presetIcons(),
        presetAttributify(),
        presetTagify(),
        presetWebFonts({
            provider: "google",
            fonts: {
                sans: "Roboto",
                mono: ["Fira Code", "Fira Mono:400,700"],
            },
        }),
    ],
});
