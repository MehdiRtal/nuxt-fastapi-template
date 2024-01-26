<template>
    <div>
        <UPageHeader title="Settings">
            <template #headline>
                <p class="text-gray-400">Dashboard</p>
                <p
                    class="i-heroicons-chevron-right-20-solid w-5 h-5 text-gray-400"
                ></p>
                <p>Settings</p>
            </template>
        </UPageHeader>
        <UPageBody> </UPageBody>
    </div>
</template>

<script setup lang="ts">
    definePageMeta({
        layout: "custom",
    });
</script>
