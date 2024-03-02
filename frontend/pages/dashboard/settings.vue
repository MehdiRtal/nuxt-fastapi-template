<template>
    <UDashboardPage>
        <UDashboardPanel grow>
            <UDashboardNavbar title="Settings" />

            <UDashboardToolbar class="py-0 px-1.5">
                <UHorizontalNavigation :links="links" />
            </UDashboardToolbar>

            <NuxtPage />
        </UDashboardPanel>
    </UDashboardPage>
</template>

<script setup lang="ts">
    definePageMeta({
        layout: "custom",
    });

    useHead({
        title: "Settings",
    });

    const links = [
        [
            {
                label: "General",
                icon: "i-heroicons-user-circle",
                to: "/dashboard/settings",
                exact: true,
            },
            {
                label: "Notifications",
                icon: "i-heroicons-bell",
                to: "/dashboard/settings/notifications",
            },
            {
                label: "Appearance",
                icon: "i-heroicons-paint-brush",
                to: "/dashboard/settings/appearance",
            },
        ],
    ];
</script>
