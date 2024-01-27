<template>
    <UCard class="max-w-sm w-full">
        <UAuthForm
            :fields="fields"
            title="Forgot password?"
            align="top"
            :ui="{footer: 'text-center'}"
        >
            <template #description>
                Please provide your email to reset your password.
            </template>
        </UAuthForm>
    </UCard>
</template>

<script setup lang="ts">
    definePageMeta({
        layout: "auth",
    });

    const fields = [
        {
            name: "email",
            type: "text",
            label: "Email",
            placeholder: "Enter your email",
            icon: "i-heroicons-envelope-solid",
            required: true,
        },
    ];
</script>
