<template>
    <div>
        <UPageHeader title="Account">
            <template #headline>
                <UBreadcrumb :links="breadcrumbLinks" />
            </template>
        </UPageHeader>
        <UPageBody>
            <div class="flex flex-col gap-2">
                <UFormGroup label="Full Name">
                    <UInput v-model="fullName" placeholder="Enter name" />
                </UFormGroup>
                <UFormGroup label="Email">
                    <UInput v-model="email" placeholder="Enter email" />
                </UFormGroup>
                <UFormGroup label="Password">
                    <UInput v-model="password" placeholder="Enter password" />
                </UFormGroup>
            </div>
            <UButton label="Update Profile" />
        </UPageBody>
    </div>
</template>

<script setup lang="ts">
    definePageMeta({
        layout: "custom",
    });

    const breadcrumbLinks = [
        {
            label: "Dashboard",
        },
        {
            label: "Account",
        },
    ];

    const fullName = ref("Mehdi Rtal");
    const email = ref("mehdirtal7@pm.me");
    const password = ref("");
</script>
