<template>
    <UDashboardPage>
        <UDashboardPanel grow>
            <UDashboardNavbar title="Home">
                <template #right>
                    <UButton
                        color="gray"
                        variant="ghost"
                        square
                        @click="isNotificationsSlideoverOpen = true"
                    >
                        <UChip color="red" inset>
                            <UIcon name="i-heroicons-bell" class="w-5 h-5" />
                        </UChip>
                    </UButton>
                </template>
            </UDashboardNavbar>

            <UDashboardPanelContent>Test</UDashboardPanelContent>
        </UDashboardPanel>

        <UDashboardSlideover
            v-model="isNotificationsSlideoverOpen"
            title="Notifications"
        />
    </UDashboardPage>
</template>

<script setup lang="ts">
    definePageMeta({
        layout: "custom",
    });

    useHead({
        title: "Home",
    });

    const isNotificationsSlideoverOpen = ref(false);
</script>
