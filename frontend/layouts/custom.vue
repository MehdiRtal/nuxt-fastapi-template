<template>
    <div>
        <UHeader>
            <template #center>
                <UDocsSearchButton label="Search..." />
            </template>

            <template #right>
                <UColorModeButton />
            </template>
        </UHeader>
        <UMain>
            <UContainer>
                <UPage>
                    <template #left>
                        <UAside :links="links">
                            <UNavigationTree
                                :links="pageLinks"
                                default-open
                                :multiple="false"
                            />
                        </UAside>
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
            label: "Documentation",
            icon: "i-heroicons-book-open",
            to: "/getting-started",
        },
        {
            label: "Playground",
            icon: "i-simple-icons-stackblitz",
            to: "/playground",
        },
        {
            label: "Roadmap",
            icon: "i-heroicons-academic-cap",
            to: "/roadmap",
        },
        {
            label: "Pro",
            icon: "i-heroicons-square-3-stack-3d",
            to: "/pro",
        },
        {
            label: "Releases",
            icon: "i-heroicons-rocket-launch",
            to: "https://github.com/nuxt/ui/releases",
            target: "_blank",
        },
    ];

    const pageLinks = [
        {
            icon: "i-heroicons-heart",
            label: "Learn how to contribute",
            to: "/getting-started/contributing",
            target: "_blank",
        },
    ];
</script>
