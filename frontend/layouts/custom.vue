<template>
    <div>
        <UHeader>
            <template #logo>Nuxt FastAPI</template>
            <template #right>
                <UPopover :popper="{placement: 'bottom-end'}">
                    <UButton
                        icon="i-heroicons-bell-solid"
                        color="gray"
                        variant="ghost"
                    />
                    <template #panel>
                        <UCard
                            :ui="{
                                strategy: 'override',
                                header: {
                                    padding: 'px-4 py-3',
                                },
                                body: {
                                    padding: 'px-4 py-3',
                                },
                            }"
                        >
                            <template #header>
                                <p class="font-medium">Notifications</p>
                            </template>
                            <UAlert
                                color="gray"
                                title="Heads up!"
                                description="You can add components to your app using the cli."
                                :close-button="{
                                    icon: 'i-heroicons-x-mark-20-solid',
                                    color: 'white',
                                    variant: 'link',
                                    padded: false,
                                }"
                                :ui="{
                                    strategy: 'override',
                                    inner: 'w-full flex-1',
                                    color: {
                                        gray: {
                                            solid: 'shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-gray-700 text-gray-700 dark:text-gray-200 bg-gray-50 hover:bg-gray-100 disabled:bg-gray-50 dark:bg-gray-800 dark:hover:bg-gray-700/50 dark:disabled:bg-gray-800 focus-visible:ring-2 focus-visible:ring-primary-500 dark:focus-visible:ring-primary-400',
                                        },
                                    },
                                }"
                            >
                            </UAlert>
                        </UCard>
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
                        <div>
                            <p class="text-left">Signed in as</p>
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
            label: "Home",
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
            to: "/dashboard/settings",
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
