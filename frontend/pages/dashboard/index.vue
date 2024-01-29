<template>
    <div>
        <UPageHeader title="Home">
            <template #headline>
                <UBreadcrumb :links="breadcrumbLinks" />
            </template>
        </UPageHeader>
        <UPageBody>
            <ULandingGrid>
                <ULandingCard
                    v-for="(module, index) in modules"
                    :key="index"
                    :title="module.title"
                    :description="module.description"
                    :icon="module.icon"
                    :class="module.class"
                />
            </ULandingGrid>
        </UPageBody>
    </div>
</template>

<script setup lang="ts">
    definePageMeta({
        layout: "custom",
    });

    const modules = [
        {
            title: "Color Palette",
            description:
                "Choose a primary and a gray color from your Tailwind CSS color palette.",
            icon: "i-heroicons-swatch",
            class: "col-span-6 row-span-2",
        },
        {
            title: "Fully Customizable",
            description:
                "Change the style of any component in your App Config or with ui prop.",
            icon: "i-heroicons-wrench-screwdriver",
            class: "col-span-6 row-span-4",
        },
        {
            title: "Icons",
            description:
                "Choose any of the 100k+ icons from the most popular icon libraries.",
            icon: "i-heroicons-face-smile",
            class: "col-span-6 row-span-4",
        },
        {
            title: "Keyboard Shortcuts",
            description:
                "Nuxt UI comes with a set of Vue composables to easily handle shortcuts.",
            icon: "i-heroicons-computer-desktop",
            class: "col-span-6 row-span-2",
        },
    ];

    const breadcrumbLinks = [
        {
            label: "Dashboard",
        },
        {
            label: "Home",
        },
    ];
</script>
