<template>
    <div>
        <UPageHeader title="Account">
            <template #headline>
                <p class="text-gray-500 dark:text-gray-400">Dashboard</p>
                <p
                    class="i-heroicons-chevron-right-20-solid w-5 h-5 text-gray-500 dark:text-gray-400"
                ></p>
                <p>Account</p>
            </template>
        </UPageHeader>
        <UPageBody></UPageBody>
    </div>
</template>

<script setup lang="ts">
    definePageMeta({
        layout: "custom",
    });
</script>
