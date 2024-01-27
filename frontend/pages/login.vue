<template>
    <UCard class="max-w-sm w-full">
        <UAuthForm
            title="Login"
            :fields="fields"
            :providers="providers"
            align="top"
            :ui="{footer: 'text-center'}"
        >
            <template #description>
                Don't have an account?
                <NuxtLink to="/register" class="text-primary font-medium"
                    >Register</NuxtLink
                >.
            </template>

            <template #password-hint>
                <NuxtLink to="/forgot-password" class="text-primary font-medium"
                    >Forgot password?</NuxtLink
                >
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
        {
            name: "password",
            label: "Password",
            type: "password",
            placeholder: "Enter your password",
            icon: "i-heroicons-lock-closed-solid",
            required: true,
        },
    ];

    const providers = [
        {
            label: "Continue with Google",
            icon: "i-mdi-google",
            color: "gray",
        },
    ];
</script>
