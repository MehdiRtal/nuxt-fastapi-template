<template>
    <div class="h-screen flex items-center justify-center flex-col gap-10">
        <p class="text-3xl font-bold">Nuxt FastAPI</p>
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
    </div>
</template>

<script setup lang="ts">
    definePageMeta({
        layout: "auth",
    });

    useHead({
        title: "Forgot Password",
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
