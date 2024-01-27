<template>
    <UCard class="max-w-sm w-full">
        <UAuthForm
            :fields="fields"
            :providers="providers"
            title="Register"
            align="top"
            :ui="{footer: 'text-center'}"
        >
            <template #description>
                Already have an account?
                <NuxtLink to="/login" class="text-primary font-medium"
                    >Login</NuxtLink
                >.
            </template>

            <template #footer>
                By signing in, you agree to our
                <NuxtLink to="#" class="text-primary font-medium"
                    >Terms of Service</NuxtLink
                >.
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
            name: "fullName",
            type: "text",
            label: "Full Name",
            placeholder: "Enter your full name",
            icon: "i-heroicons-user-solid",
            required: true,
        },
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
