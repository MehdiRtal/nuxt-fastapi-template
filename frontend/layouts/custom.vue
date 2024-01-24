<template>
    <div>
        <UHeader>
            <template #logo>Nuxt FastAPI</template>
            <template #right>
                <UPopover>
                    <UButton
                        icon="i-heroicons-bell-solid"
                        color="gray"
                        variant="ghost"
                    />
                    <template #panel>
                        <div class="p-4"></div>
                    </template>
                </UPopover>
                <UDropdown
                    :items="account"
                    :popper="{placement: 'bottom-start'}"
                >
                    <UButton
                        icon="i-heroicons-user-solid"
                        color="gray"
                        variant="ghost"
                    />
                    <template #account="{item}">
                        <div class="text-left">
                            <p>Signed in as</p>
                            <p class="font-medium dark:text-white">
                                {{ item.label }}
                            </p>
                        </div>
                    </template>
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
            icon: "i-heroicons-home",
            to: "/dashboard",
        },
        {
            label: "Items",
            icon: "i-heroicons-square-3-stack-3d",
            to: "/dashboard/items",
        },
    ];

    const pageLinks = [
        {
            label: "Settings",
            icon: "i-heroicons-cog",
            to: "/",
        },
    ];

    const account = [
        [
            {
                label: "ben@example.com",
                slot: "account",
                disabled: true,
            },
        ],
        [
            {
                label: "Logout",
                icon: "i-heroicons-arrow-left-on-rectangle",
            },
        ],
    ];
</script>
