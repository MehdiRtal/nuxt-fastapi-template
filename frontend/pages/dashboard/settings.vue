<template>
    <div>
        <UPageHeader title="Settings">
            <template #headline>
                <p class="text-gray-500 dark:text-gray-400">Dashboard</p>
                <p
                    class="i-heroicons-chevron-right-20-solid w-5 h-5 text-gray-500 dark:text-gray-400"
                ></p>
                <p>Settings</p>
            </template>
        </UPageHeader>
        <UPageBody>
            <div class="flex justify-start items-center gap-2">
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
</script>
