<template>
    <UDashboardPanelContent class="pb-24">
        <UForm
            :state="state"
            :validate="validate"
            :validate-on="['submit']"
            @submit="onSubmit"
        >
            <UDashboardSection
                title="Profile"
                description="This information will be displayed publicly so be careful what you share."
            >
                <template #links>
                    <UButton type="submit" label="Save changes" />
                </template>

                <UFormGroup
                    name="name"
                    label="Name"
                    description="Will appear on receipts, invoices, and other communication."
                    required
                    class="grid grid-cols-2 gap-2 items-center"
                    :ui="{container: ''}"
                >
                    <UInput
                        v-model="state.name"
                        autocomplete="off"
                        icon="i-heroicons-user"
                        size="md"
                    />
                </UFormGroup>

                <UFormGroup
                    name="email"
                    label="Email"
                    description="Used to sign in, for email receipts and product updates."
                    required
                    class="grid grid-cols-2 gap-2"
                    :ui="{container: ''}"
                >
                    <UInput
                        v-model="state.email"
                        type="email"
                        autocomplete="off"
                        icon="i-heroicons-envelope"
                        size="md"
                    />
                </UFormGroup>

                <UFormGroup
                    name="username"
                    label="Username"
                    description="Your unique username for logging in and your profile URL."
                    required
                    class="grid grid-cols-2 gap-2"
                    :ui="{container: ''}"
                >
                    <UInput
                        v-model="state.username"
                        type="username"
                        autocomplete="off"
                        size="md"
                        input-class="ps-[77px]"
                    >
                        <template #leading>
                            <span
                                class="text-gray-500 dark:text-gray-400 text-sm"
                                >nuxt.com/</span
                            >
                        </template>
                    </UInput>
                </UFormGroup>

                <UFormGroup
                    name="avatar"
                    label="Avatar"
                    class="grid grid-cols-2 gap-2"
                    help="JPG, GIF or PNG. 1MB Max."
                    :ui="{
                        container: 'flex flex-wrap items-center gap-3',
                        help: 'mt-0',
                    }"
                >
                    <UAvatar :src="state.avatar" :alt="state.name" size="lg" />

                    <UButton
                        label="Choose"
                        color="white"
                        size="md"
                        @click="onFileClick"
                    />

                    <UInput
                        ref="fileRef"
                        type="file"
                        class="hidden"
                        accept=".jpg, .jpeg, .png, .gif"
                        @change="onFileChange"
                    />
                </UFormGroup>

                <UFormGroup
                    name="bio"
                    label="Bio"
                    description="Brief description for your profile. URLs are hyperlinked."
                    class="grid grid-cols-2 gap-2"
                    :ui="{container: ''}"
                >
                    <UTextarea
                        v-model="state.bio"
                        :rows="5"
                        autoresize
                        size="md"
                    />
                </UFormGroup>

                <UFormGroup
                    name="password"
                    label="Password"
                    description="Confirm your current password before setting a new one."
                    class="grid grid-cols-2 gap-2"
                    :ui="{container: ''}"
                >
                    <UInput
                        id="password"
                        v-model="state.password_current"
                        type="password"
                        placeholder="Current password"
                        size="md"
                    />
                    <UInput
                        id="password_new"
                        v-model="state.password_new"
                        type="password"
                        placeholder="New password"
                        size="md"
                        class="mt-2"
                    />
                </UFormGroup>
            </UDashboardSection>
        </UForm>

        <UDivider class="mb-4" />

        <UDashboardSection
            title="Account"
            description="No longer want to use our service? You can delete your account here. This action is not reversible. All information related to this account will be deleted permanently."
        >
            <template #links>
                <UButton
                    color="red"
                    label="Delete account"
                    size="md"
                    @click="isDeleteAccountModalOpen = true"
                />
            </template>
        </UDashboardSection>

        <UDashboardModal
            v-model="isDeleteAccountModalOpen"
            title="Delete account"
            description="Are you sure you want to delete your account?"
            icon="i-heroicons-exclamation-circle"
            prevent-close
            :close-button="null"
            :ui="{
                icon: {
                    base: 'text-red-500 dark:text-red-400',
                },
                footer: {
                    base: 'ml-16',
                },
            }"
        >
            <template #footer>
                <UButton
                    color="white"
                    label="Cancel"
                    @click="isDeleteAccountModalOpen = false"
                />
                <UButton
                    color="red"
                    label="Delete"
                    :loading="loading"
                    @click="onDelete"
                />
            </template>
        </UDashboardModal>
    </UDashboardPanelContent>
</template>

<script setup lang="ts">
    const state = reactive({
        name: "Benjamin Canac",
        email: "ben@nuxtlabs.com",
        username: "benjamincanac",
        avatar: "",
        bio: "",
        password_current: "",
        password_new: "",
    });

    const isDeleteAccountModalOpen = ref(false);

    const validate = (state) => {
        const errors = [];
        if (!state.name)
            errors.push({path: "name", message: "Please enter your name."});
        if (!state.email)
            errors.push({path: "email", message: "Please enter your email."});
        if (
            (state.password_current && !state.password_new) ||
            (!state.password_current && state.password_new)
        )
            errors.push({
                path: "password",
                message: "Please enter a valid password.",
            });
        return errors;
    };

    function onFileChange(e: Event) {
        const input = e.target as HTMLInputElement;

        if (!input.files?.length) {
            return;
        }

        state.avatar = URL.createObjectURL(input.files[0]);
    }

    function onFileClick() {
        fileRef.value?.input.click();
    }

    function onSubmit(event) {
        console.log(event.data);

        toast.add({title: "Profile updated", icon: "i-heroicons-check-circle"});
    }

    const toast = useToast();

    const loading = ref(false);

    function onDelete() {
        loading.value = true;

        setTimeout(() => {
            loading.value = false;
            toast.add({
                icon: "i-heroicons-check-circle",
                title: "Your account has been deleted",
                color: "red",
            });
            isDeleteAccountModalOpen.value = false;
        }, 2000);
    }
</script>
