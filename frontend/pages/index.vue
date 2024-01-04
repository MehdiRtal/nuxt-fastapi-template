<template>
    <div class="h-screen flex items-center justify-center">
        <div>
            <UTabs :items="items" class="w-96 h-96">
                <template #item="{item}">
                    <UCard>
                        <div v-if="item.key === 'signup'" class="space-y-3">
                            <div class="flex flex-row gap-4">
                                <div class="grow">
                                    <UFormGroup label="First Name" required>
                                        <UInput placeholder="John" />
                                    </UFormGroup>
                                </div>
                                <div class="grow">
                                    <UFormGroup label="Last Name" required>
                                        <UInput placeholder="Doe" />
                                    </UFormGroup>
                                </div>
                            </div>
                            <UFormGroup label="Email" required>
                                <UInput placeholder="john.doe@example.com" />
                            </UFormGroup>
                            <UFormGroup label="Password" required>
                                <UButtonGroup>
                                    <UInput
                                        :type="
                                            showPassword ? 'text' : 'password'
                                        "
                                    />
                                    <UButton
                                        :icon="
                                            showPassword
                                                ? 'i-mdi-eye-off'
                                                : 'i-mdi-eye'
                                        "
                                        color="gray"
                                        @click="showPassword = !showPassword"
                                    />
                                </UButtonGroup>
                            </UFormGroup>
                            <UFormGroup
                                v-if="!showPassword"
                                label="Confirm Password"
                                required
                            >
                                <UInput type="password" />
                            </UFormGroup>
                            <UButton type="submit" block>Sign Up</UButton>
                            <UDivider label="OR" color="gray" />
                            <UButton
                                color="gray"
                                label="Sign Up with GitHub"
                                icon="i-simple-icons-github"
                                block
                            />
                            <UButton
                                color="gray"
                                label="Sign Up with Google"
                                icon="i-simple-icons-google"
                                block
                            />
                        </div>
                        <div v-else-if="item.key === 'login'" class="space-y-3">
                            <UFormGroup label="Email" required>
                                <UInput placeholder="john.doe@example.com" />
                            </UFormGroup>
                            <UFormGroup label="Password" required>
                                <UButtonGroup>
                                    <UInput
                                        :type="
                                            showPassword ? 'text' : 'password'
                                        "
                                    />
                                    <UButton
                                        :icon="
                                            showPassword
                                                ? 'i-mdi-eye-off'
                                                : 'i-mdi-eye'
                                        "
                                        color="gray"
                                        @click="showPassword = !showPassword"
                                    />
                                </UButtonGroup>
                            </UFormGroup>
                            <UButton type="submit" block>Log In</UButton>
                            <UDivider label="OR" color="gray" />
                            <UButton
                                color="gray"
                                label="Log In with GitHub"
                                icon="i-simple-icons-github"
                                block
                            />
                            <UButton
                                color="gray"
                                label="Log In with Google"
                                icon="i-simple-icons-google"
                                block
                            />
                        </div>
                    </UCard>
                </template>
            </UTabs>
        </div>
    </div>
</template>

<script setup>
    const items = [
        {
            key: "signup",
            label: "Sign Up",
        },
        {
            key: "login",
            label: "Log In",
        },
    ];

    const showPassword = ref(false);
</script>
