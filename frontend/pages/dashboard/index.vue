<template>
    <div>
        <UPageHeader title="Overview" />
        <UPageBody>
            <UPageGrid>
                <UPageCard
                    v-for="(module, index) in modules"
                    :key="index"
                    v-bind="module"
                >
                    <template #description>
                        <span>{{ module.description }}</span>
                    </template>
                </UPageCard>
            </UPageGrid>
        </UPageBody>
    </div>
</template>

<script setup lang="ts">
    definePageMeta({
        layout: "custom",
    });

    const modules = [
        {
            title: "VueUse",
            description:
                "Collection of essential Vue Composition Utilities for Vue 2 and 3.",
        },
        {
            title: "ESLint",
            description: "ESLint module for Nuxt.",
        },
        {
            title: "Tailwind CSS",
            description:
                "Add Tailwind CSS to your Nuxt application in seconds with PurgeCSS included for minimal CSS.",
        },
    ];
</script>
