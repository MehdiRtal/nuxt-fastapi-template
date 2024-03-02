<template>
    <UDashboardLayout>
        <UDashboardPanel :width="300" collapsible>
            <UDashboardNavbar title="Nuxt FastAPI" />

            <UDashboardSidebar>
                <UDashboardSidebarLinks :links="links" />

                <div class="flex-1" />

                <UDashboardSidebarLinks :links="footerLinks" />

                <UDivider />

                <template #footer>
                    <UDropdown
                        mode="hover"
                        :items="items"
                        :ui="{
                            width: 'w-full',
                            item: {disabled: 'cursor-text select-text'},
                        }"
                        :popper="{strategy: 'absolute', placement: 'top'}"
                        class="w-full"
                    >
                        <template #default="{open}">
                            <UButton
                                color="gray"
                                variant="ghost"
                                class="w-full"
                                label="Mehdi Rtal"
                                :class="[open && 'bg-gray-50 dark:bg-gray-800']"
                            >
                                <template #leading>
                                    <UAvatar
                                        src="https://avatars.githubusercontent.com/u/739984?v=4"
                                        alt="M"
                                        size="xs"
                                    />
                                </template>

                                <template #trailing>
                                    <UIcon
                                        name="i-heroicons-ellipsis-vertical"
                                        class="w-5 h-5 ml-auto"
                                    />
                                </template>
                            </UButton>
                        </template>

                        <template #account>
                            <div class="text-left">
                                <p>Signed in as</p>
                                <p
                                    class="truncate font-medium text-gray-900 dark:text-white"
                                >
                                    mehdirtal7@pm.me
                                </p>
                            </div>
                        </template>
                    </UDropdown>
                </template>
            </UDashboardSidebar>
        </UDashboardPanel>
        <slot />
    </UDashboardLayout>
</template>

<script setup lang="ts">
    // useHead({
    //     bodyAttrs: {
    //         class: "bg-gray-50 dark:bg-gray-950",
    //     },
    // });

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

    const footerLinks = [
        {
            label: "Documentation",
            icon: "i-heroicons-book-open",
            to: "https://ui.nuxt.com/pro/getting-started",
        },
        {
            label: "Help & Support",
            icon: "i-heroicons-question-mark-circle",
            target: "_blank",
        },
    ];

    const items = ref([
        [
            {
                slot: "account",
                label: "",
                disabled: true,
            },
        ],
        [
            {
                label: "Settings",
                icon: "i-heroicons-cog-8-tooth",
                to: "/dashboard/settings",
            },
        ],
        [
            {
                label: "Log out",
                icon: "i-heroicons-arrow-left-on-rectangle",
            },
        ],
    ]);
</script>
