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
            name: "firstName",
            type: "text",
            label: "First Name",
            placeholder: "Enter your first name",
            required: true,
        },
        {
            name: "lastName",
            type: "text",
            label: "Last Name",
            placeholder: "Enter your last name",
            required: true,
        },
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
            color: "gray",
        },
    ];
</script>
