<template>
    <div class="h-screen flex items-center justify-center flex-col gap-10">
        <p class="text-3xl font-bold">Nuxt FastAPI</p>
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
                    <NuxtLink
                        to="/forgot-password"
                        class="text-primary font-medium"
                        >Forgot password?</NuxtLink
                    >
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
        title: "Login",
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
