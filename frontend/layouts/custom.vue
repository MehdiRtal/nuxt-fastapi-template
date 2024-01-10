<template>
    <div>
        <UHeader>
            <template #logo>Nuxt FastAPI</template>
            <template #right>
                <UDocsSearchButton label="" />
                <UColorModeButton />
                <UButton
                    icon="i-heroicons-bell-solid"
                    color="gray"
                    variant="ghost"
                />
                <UButton
                    icon="i-heroicons-user-solid"
                    color="gray"
                    variant="ghost"
                />
            </template>
        </UHeader>
        <UMain>
            <UContainer>
                <UPage>
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
            label: "Overview",
            icon: "i-heroicons-home",
            to: "/",
        },
    ];
</script>
