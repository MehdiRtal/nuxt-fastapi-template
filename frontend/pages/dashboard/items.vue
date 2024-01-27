<template>
    <div>
        <UPageHeader title="Items">
            <template #headline>
                <p class="text-gray-500 dark:text-gray-400">Dashboard</p>
                <p
                    class="i-heroicons-chevron-right-20-solid w-5 h-5 text-gray-500 dark:text-gray-400"
                ></p>
                <p>Items</p>
            </template>
        </UPageHeader>
        <UPageBody>
            <div
                class="border rounded-md bg-white dark:border-gray-800 dark:bg-gray-900"
            >
                <div
                    class="flex justify-between px-7 py-3.5 border-b dark:border-gray-700"
                >
                    <UInput
                        v-model="q"
                        icon="i-heroicons-magnifying-glass-solid"
                        placeholder="Search..."
                    />
                    <UButton
                        icon="i-heroicons-plus"
                        label="Add"
                        color="primary"
                        @click="isAddOpen = true"
                    />
                </div>
                <UTable
                    :rows="filteredRows"
                    :columns="columns"
                    :ui="{
                        th: {
                            padding: 'pl-8',
                        },
                        td: {
                            padding: 'pl-8',
                        },
                    }"
                >
                    <template #actions-data="{row}">
                        <UDropdown :items="items(row)">
                            <UButton
                                color="gray"
                                icon="i-heroicons-ellipsis-horizontal-solid"
                            />
                        </UDropdown>
                    </template>
                </UTable>
                <div
                    v-if="filteredRows.length > 0"
                    class="flex justify-end px-7 py-3.5 border-t dark:border-gray-800"
                >
                    <UPagination
                        v-model="page"
                        :page-count="pageCount"
                        :total="people.length"
                        :next-button="{
                            color: 'gray',
                        }"
                        :prev-button="{
                            color: 'gray',
                        }"
                        :inactive-button="{
                            color: 'gray',
                        }"
                    />
                </div>
            </div>
        </UPageBody>
        <UModal
            v-model="isAddOpen"
            prevent-close
            :ui="{
                width: 'sm:max-w-md',
            }"
        >
            <UCard
                :ui="{
                    strategy: 'override',
                    header: {
                        padding: 'px-4 py-3',
                    },
                    body: {
                        padding: 'px-4 py-3',
                    },
                }"
            >
                <template #header>
                    <p class="font-semibold">Add Item</p>
                </template>
                <div class="flex flex-col space-y-4">
                    <UFormGroup label="Name">
                        <UInput placeholder="Enter name" />
                    </UFormGroup>
                    <div class="flex justify-end gap-1.5">
                        <UButton
                            label="Cancel"
                            color="gray"
                            @click="isAddOpen = false"
                        />
                        <UButton label="Continue" />
                    </div>
                </div>
            </UCard>
        </UModal>
        <UModal
            v-model="isDeleteOpen"
            prevent-close
            :ui="{
                width: 'sm:max-w-md',
            }"
        >
            <UCard
                :ui="{
                    strategy: 'override',
                    header: {
                        padding: 'px-4 py-3',
                    },
                    body: {
                        padding: 'px-4 py-3',
                    },
                }"
            >
                <template #header>
                    <p class="font-semibold">Delete Item</p>
                </template>
                <div class="flex flex-col space-y-4">
                    <p>Are you sure you want to delete this item?</p>
                    <div class="flex justify-end gap-1.5">
                        <UButton
                            label="Cancel"
                            color="gray"
                            @click="isDeleteOpen = false"
                        />
                        <UButton label="Continue" />
                    </div>
                </div>
            </UCard>
        </UModal>
        <UModal
            v-model="isEditOpen"
            prevent-close
            :ui="{
                width: 'sm:max-w-md',
            }"
        >
            <UCard
                :ui="{
                    strategy: 'override',
                    header: {
                        padding: 'px-4 py-3',
                    },
                    body: {
                        padding: 'px-4 py-3',
                    },
                }"
            >
                <template #header>
                    <p class="font-semibold">Edit Item</p>
                </template>
                <div class="flex flex-col space-y-4">
                    <UFormGroup label="Name">
                        <UInput placeholder="Enter name" />
                    </UFormGroup>
                    <div class="flex justify-end gap-1.5">
                        <UButton
                            label="Cancel"
                            color="gray"
                            @click="isEditOpen = false"
                        />
                        <UButton label="Continue" />
                    </div>
                </div>
            </UCard>
        </UModal>
    </div>
</template>

<script setup lang="ts">
    definePageMeta({
        layout: "custom",
    });

    const columns = [
        {
            key: "id",
            label: "ID",
        },
        {
            key: "name",
            label: "Name",
            sortable: true,
        },
        {
            key: "title",
            label: "Title",
            sortable: true,
        },
        {
            key: "email",
            label: "Email",
            sortable: true,
        },
        {
            key: "role",
            label: "Role",
            sortable: true,
        },
        {
            key: "actions",
        },
    ];

    const people = [
        {
            id: 1,
            name: "Lindsay Walton",
            title: "Front-end Developer",
            email: "lindsay.walton@example.com",
            role: "Member",
        },
        {
            id: 2,
            name: "Courtney Henry",
            title: "Designer",
            email: "courtney.henry@example.com",
            role: "Admin",
        },
        {
            id: 3,
            name: "Tom Cook",
            title: "Director of Product",
            email: "tom.cook@example.com",
            role: "Member",
        },
        {
            id: 4,
            name: "Whitney Francis",
            title: "Copywriter",
            email: "whitney.francis@example.com",
            role: "Admin",
        },
        {
            id: 5,
            name: "Leonard Krasner",
            title: "Senior Designer",
            email: "leonard.krasner@example.com",
            role: "Owner",
        },
        {
            id: 6,
            name: "Floyd Miles",
            title: "Principal Designer",
            email: "floyd.miles@example.com",
            role: "Member",
        },
    ];

    const items = (row) => [
        [
            {
                label: "Edit",
                icon: "i-heroicons-pencil-square-20-solid",
                click: () => (isEditOpen.value = true),
            },
            {
                label: "Delete",
                icon: "i-heroicons-trash-20-solid",
                click: () => (isDeleteOpen.value = true),
            },
        ],
    ];

    const rows = computed(() => {
        return people.slice(
            (page.value - 1) * pageCount,
            page.value * pageCount,
        );
    });

    const filteredRows = computed(() => {
        if (!q.value) {
            return rows.value;
        }
        return people.filter((rows) => {
            return Object.values(rows).some((value) => {
                return String(value)
                    .toLowerCase()
                    .includes(q.value.toLowerCase());
            });
        });
    });

    const page = ref(1);
    const pageCount = 12;

    const q = ref("");

    const isAddOpen = ref(false);
    const isDeleteOpen = ref(false);
    const isEditOpen = ref(false);
</script>
