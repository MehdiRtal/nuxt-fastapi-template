<template>
    <div class="h-screen flex items-center justify-center">
        <slot />
    </div>
</template>

<script setup lang="ts">
    useHead({
        bodyAttrs: {
            class: "bg-gray-50 dark:bg-gray-950",
        },
    });
</script>
