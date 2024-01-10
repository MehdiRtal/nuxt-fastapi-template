<template>
    <div>
        <UHeader>
            <template #logo>Nuxt FastAPI</template>
            <template #right>
                <UDocsSearchButton label="" />
                <UColorModeButton />
            </template>
        </UHeader>
        <UMain>
            <UContainer>
                <UPage>
                    <UPageHeader
                        headline="Page"
                        title="PageHeader"
                        description="A responsive header for your pages."
                    />

                    <template #left>
                        <UAside :links="links" />
                    </template>
                    <slot />
                </UPage>
            </UContainer>
        </UMain>
        <UFooter />
    </div>
</template>

<script setup lang="ts">
    const links = [
        {
            label: "Installation",
            icon: "i-heroicons-home",
            to: "/getting-started/installation",
        },
        {
            label: "Vertical Navigation",
            icon: "i-heroicons-chart-bar",
            to: "/navigation/vertical-navigation",
        },
        {
            label: "Command Palette",
            icon: "i-heroicons-command-line",
            to: "/navigation/command-palette",
        },
    ];
</script>
