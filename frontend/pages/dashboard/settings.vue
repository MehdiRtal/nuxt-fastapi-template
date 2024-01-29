<template>
    <div>
        <UPageHeader title="Settings">
            <template #headline>
                <UBreadcrumb :links="breadcrumbLinks" />
            </template>
        </UPageHeader>
        <UPageBody>
            <div class="flex justify-start items-end gap-4">
                <p class="font-medium">Color mode:</p>
                <UColorModeSelect class="w-32" />
            </div>
        </UPageBody>
    </div>
</template>

<script setup lang="ts">
    definePageMeta({
        layout: "custom",
    });

    const breadcrumbLinks = [
        {
            label: "Dashboard",
        },
        {
            label: "Settings",
        },
    ];
</script>
