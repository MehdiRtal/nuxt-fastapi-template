<template>
    <UDashboardPage>
        <UDashboardPanel grow>
            <UDashboardNavbar title="Items" :badge="items.length">
                <template #right>
                    <UInput
                        ref="input"
                        v-model="q"
                        icon="i-heroicons-funnel"
                        autocomplete="off"
                        placeholder="Filter items..."
                    />

                    <UButton
                        label="New item"
                        trailing-icon="i-heroicons-plus"
                        color="gray"
                        @click="isNewItemModalOpen = true"
                    />
                </template>
            </UDashboardNavbar>

            <UDashboardModal
                v-model="isNewItemModalOpen"
                title="New item"
                description="Add a new item to your database"
            >
                <UForm
                    :validate="validate"
                    :validate-on="['submit']"
                    :state="state"
                    class="space-y-4"
                    @submit="onSubmit"
                >
                    <UFormGroup label="Name" name="name">
                        <UInput
                            v-model="state.name"
                            placeholder="John Doe"
                            autofocus
                        />
                    </UFormGroup>

                    <UFormGroup label="Email" name="email">
                        <UInput
                            v-model="state.email"
                            type="email"
                            placeholder="john.doe@example.com"
                        />
                    </UFormGroup>

                    <div class="flex justify-end gap-1.5">
                        <UButton
                            label="Cancel"
                            color="white"
                            @click="isNewItemModalOpen = false"
                        />
                        <UButton type="submit" label="Save" />
                    </div>
                </UForm>
            </UDashboardModal>

            <UTable
                v-model="selected"
                :rows="rows"
                :columns="columns"
                :loading="pending"
                :ui="{divide: 'divide-gray-200 dark:divide-gray-800'}"
                @select="onSelect"
            />
        </UDashboardPanel>
    </UDashboardPage>
</template>

<script lang="ts" setup>
    definePageMeta({
        layout: "custom",
    });

    useHead({
        title: "Items",
    });

    const columns = [
        {
            key: "id",
            label: "ID",
        },
        {
            key: "name",
            label: "Name",
        },
        {
            key: "user_id",
            label: "User ID",
        },
    ];

    const q = ref("");
    const selected = ref([]);
    const isNewItemModalOpen = ref(false);

    const {data: items, pending} = await $api("/items");

    const rows = computed(() => {
        if (!q.value) {
            return items;
        }

        return items.filter((items) => {
            return Object.values(items).some((value) => {
                return String(value)
                    .toLowerCase()
                    .includes(q.value.toLowerCase());
            });
        });
    });

    function onSelect(row) {
        const index = selected.value.findIndex((item) => item.id === row.id);
        if (index === -1) {
            selected.value.push(row);
        } else {
            selected.value.splice(index, 1);
        }
    }

    const state = reactive({
        name: undefined,
        email: undefined,
    });

    const validate = (state) => {
        const errors = [];
        if (!state.name)
            errors.push({path: "name", message: "Please enter a name."});
        if (!state.email)
            errors.push({path: "email", message: "Please enter an email."});
        return errors;
    };

    const toast = useToast();

    const loading = ref(false);

    function onSubmit(event) {
        console.log(event.data);

        setTimeout(() => {
            loading.value = false;
            toast.add({
                icon: "i-heroicons-check-circle",
                title: "Your item has been added",
                color: "green",
            });
            isNewItemModalOpen.value = false;
        }, 2000);
    }
</script>
