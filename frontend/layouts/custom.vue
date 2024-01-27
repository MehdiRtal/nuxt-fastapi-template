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
                                <p class="font-semibold">Notifications</p>
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
                                            solid: 'shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-gray-700 text-gray-700 dark:text-gray-200 bg-gray-50 dark:bg-gray-800',
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
                        <UAside>
                            <template #links>
                                <UAsideLinks :links="topLinks" />
                            </template>
                            <template #bottom>
                                <UDivider class="my-6" />
                                <UAsideLinks :links="bottomLinks" />
                            </template>
                        </UAside>
                    </template>
                    <slot />
                </UPage>
            </UContainer>
        </UMain>
    </div>
</template>

<script setup lang="ts">
    useHead({
        bodyAttrs: {
            class: "bg-gray-50 dark:bg-gray-950",
        },
    });

    const topLinks = [
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

    const bottomLinks = [
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
