<template>
    <div>
        <UHeader>
            <template #logo>Nuxt FastAPI</template>
            <template #right>
                <UDocsSearchButton label="" />
                <UDropdown :items="links" :popper="{placement: 'bottom-start'}">
                    <UButton
                        icon="i-heroicons-bell-solid"
                        color="gray"
                        variant="ghost"
                    />
                </UDropdown>
                <UDropdown :items="links" :popper="{placement: 'bottom-start'}">
                    <UButton
                        icon="i-heroicons-user-solid"
                        color="gray"
                        variant="ghost"
                    />
                </UDropdown>
            </template>
        </UHeader>
        <UMain>
            <UContainer>
                <UPage>
                    <template #left>
                        <UAside :links="links">
                            <template #bottom>
                                <UDivider class="my-6" />

                                <UAsideLinks :links="pageLinks" />
                            </template>
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
    useHead({
        bodyAttrs: {
            class: "dark:bg-gray-950",
        },
    });

    const links = [
        {
            label: "Overview",
            icon: "i-heroicons-square-3-stack-3d",
            to: "/",
        },
    ];

    const pageLinks = [
        {
            label: "Settings",
            icon: "i-heroicons-cog",
            to: "/",
        },
    ];
</script>
