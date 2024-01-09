<template>
    <div class="flex items-center justify-center h-screen">
        <UCard class="max-w-sm w-full">
            <UAuthForm
                :fields="fields"
                :providers="providers"
                title="Welcome back!"
                align="top"
                icon="i-heroicons-lock-closed"
                :ui="{base: 'text-center', footer: 'text-center'}"
                @submit="onSubmit"
            >
                <template #description>
                    Don't have an account?
                    <NuxtLink to="/" class="text-primary font-medium"
                        >Sign up</NuxtLink
                    >.
                </template>

                <template #password-hint>
                    <NuxtLink to="/" class="text-primary font-medium"
                        >Forgot password?</NuxtLink
                    >
                </template>

                <template #footer>
                    By signing in, you agree to our
                    <NuxtLink to="/" class="text-primary font-medium"
                        >Terms of Service</NuxtLink
                    >.
                </template>
            </UAuthForm>
        </UCard>
    </div>
</template>

<script setup lang="ts">
    const fields = [
        {
            name: "email",
            type: "text",
            label: "Email",
            placeholder: "Enter your email",
            required: true,
        },
        {
            name: "password",
            label: "Password",
            type: "password",
            placeholder: "Enter your password",
            required: true,
        },
    ];

    const providers = [
        {
            label: "Continue with Google",
            icon: "i-mdi-google",
            color: "white",
            click: () => {
                console.log("Redirect to Google");
            },
        },
    ];

    function onSubmit(data) {
        console.log("Submitted", data);
    }
</script>
