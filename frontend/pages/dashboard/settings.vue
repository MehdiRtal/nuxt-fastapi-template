<template>
    <div>
        <UPageHeader title="Settings">
            <template #headline>
                <UBreadcrumb :links="breadcrumbLinks" />
            </template>
        </UPageHeader>
        <UPageBody>
            <UTabs
                :items="items"
                orientation="vertical"
                :ui="{
                    strategy: 'override',
                    wrapper: 'flex items-start gap-7',
                    list: {
                        background: '',
                        width: 'w-1/4',
                        tab: {
                            base: 'relative inline-flex items-center justify-start flex-shrink-0 w-full ui-focus-visible:outline-0 ui-focus-visible:ring-2 ui-focus-visible:ring-primary-500 dark:ui-focus-visible:ring-primary-400 ui-not-focus-visible:outline-none focus:outline-none disabled:cursor-not-allowed disabled:opacity-75 transition-colors duration-200 ease-out',
                            active: 'dark:text-white dark:bg-gray-900 border border-gray-250 dark:border-gray-800',
                        },
                    },
                }"
            >
                <template #default="{item}">
                    <div class="flex items-center gap-2">
                        <UIcon :name="item.icon" class="w-4 h-4" />
                        <span>{{ item.label }}</span>
                    </div>
                </template>
                <template #item="{item}">
                    <UCard
                        :ui="{
                            strategy: 'override',
                            header: {
                                padding: 'px-4 py-3',
                            },
                            body: {
                                padding: 'px-4 py-4 pb-6',
                            },
                            footer: {
                                padding: 'px-4 py-3',
                            },
                        }"
                    >
                        <template #header>
                            <p
                                class="font-semibold text-gray-900 dark:text-white"
                            >
                                {{ item.label }}
                            </p>
                        </template>
                        <div v-if="item.key === 'general'" class="space-y-3">
                            <UFormGroup label="Full Name">
                                <UInput
                                    v-model="generalForm.fullName"
                                    placeholder="Enter name"
                                />
                            </UFormGroup>
                            <UFormGroup label="Email">
                                <UInput
                                    v-model="generalForm.email"
                                    placeholder="Enter email"
                                />
                            </UFormGroup>
                        </div>
                        <div
                            v-else-if="item.key === 'security'"
                            class="space-y-3"
                        >
                            <UFormGroup label="Current Password">
                                <UInput
                                    v-model="passwordForm.currentPassword"
                                    placeholder="Enter current password"
                                />
                            </UFormGroup>
                            <div class="flex gap-2">
                                <UFormGroup class="w-full" label="New Password">
                                    <UInput
                                        v-model="passwordForm.newPassword"
                                        placeholder="Enter new password"
                                    />
                                </UFormGroup>
                                <UFormGroup
                                    class="w-full"
                                    label="Confirm New Password"
                                >
                                    <UInput
                                        v-model="passwordForm.newPassword"
                                        placeholder="Confirm new password"
                                    />
                                </UFormGroup>
                            </div>
                        </div>
                        <div v-else-if="item.key === 'appareance'">
                            <div class="flex justify-start items-center gap-2">
                                <p class="font-medium text-sm">Color mode</p>
                                <UColorModeSelect class="w-32" />
                            </div>
                        </div>
                        <template #footer>
                            <div class="flex justify-end">
                                <UButton type="submit" color="primary"
                                    >Save Changes</UButton
                                >
                            </div>
                        </template>
                    </UCard>
                </template>
            </UTabs>
        </UPageBody>
    </div>
</template>

<script setup lang="ts">
    definePageMeta({
        layout: "custom",
    });

    useHead({
        title: "Settings",
    });

    const breadcrumbLinks = [
        {
            label: "Dashboard",
        },
        {
            label: "Settings",
        },
    ];

    const items = [
        {
            key: "general",
            label: "General",
            icon: "i-heroicons-user",
        },
        {
            key: "security",
            label: "Security",
            icon: "i-heroicons-lock-closed",
        },
        {
            key: "notifications",
            label: "Notifications",
            icon: "i-heroicons-bell",
        },
        {
            key: "integrations",
            label: "Integrations",
            icon: "i-heroicons-link",
        },
        {
            key: "billing",
            label: "Billing",
            icon: "i-heroicons-credit-card",
        },
        {
            key: "appareance",
            label: "Appareance",
            icon: "i-heroicons-paint-brush",
        },
    ];

    const generalForm = ref({
        fullName: "Mehdi Rtal",
        email: "mehdirtal7@pm.me",
    });

    const passwordForm = ref({currentPassword: "", newPassword: ""});
</script>
