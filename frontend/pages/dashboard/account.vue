<template>
    <div>
        <UPageHeader title="Account">
            <template #headline>
                <UBreadcrumb :links="breadcrumbLinks" />
            </template>
        </UPageHeader>
        <UPageBody>
            <h2 class="text-2xl font-bold text-white my-6">General</h2>
            <div class="flex flex-col gap-4">
                <UFormGroup label="Full Name">
                    <UInput v-model="fullName" placeholder="Enter name" />
                </UFormGroup>
                <UFormGroup label="Email">
                    <UInput v-model="email" placeholder="Enter email" />
                </UFormGroup>
                <div class="flex justify-end">
                    <UButton label="Save Changes" />
                </div>
            </div>
            <h2 class="text-2xl font-bold text-white my-6">Identity</h2>
            <div class="flex flex-col gap-4">
                <UFormGroup label="Full Name">
                    <UInput v-model="fullName" placeholder="Enter name" />
                </UFormGroup>
                <UFormGroup label="Email">
                    <UInput v-model="email" placeholder="Enter email" />
                </UFormGroup>
                <div class="flex justify-end">
                    <UButton label="Save Changes" />
                </div>
            </div>
            <h2 class="text-2xl font-bold text-white my-6">Security</h2>
            <div class="flex flex-col gap-4">
                <UFormGroup label="Current Password">
                    <UInput placeholder="Enter current password" />
                </UFormGroup>
                <div class="flex gap-1.5">
                    <UFormGroup class="w-full" label="New Password">
                        <UInput placeholder="Enter new password" />
                    </UFormGroup>
                    <UFormGroup class="w-full" label="Confirm New Password">
                        <UInput
                            v-model="password"
                            placeholder="Confirm new password"
                        />
                    </UFormGroup>
                </div>
                <div class="flex justify-end">
                    <UButton label="Save Changes" />
                </div>
            </div>
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
