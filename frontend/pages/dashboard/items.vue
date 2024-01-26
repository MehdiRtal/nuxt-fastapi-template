<template>
    <div>
        <UPageHeader title="Items">
            <template #headline>
                <p class="text-gray-400 truncate">Dashboard</p>
                <p
                    class="i-heroicons-chevron-right-20-solid w-5 h-5 text-gray-400"
                ></p>
                <p>Items</p>
            </template>
        </UPageHeader>
        <UPageBody>
            <div
                class="border rounded-md dark:border-gray-800 dark:bg-gray-900"
            >
                <div
                    class="flex justify-between px-7 py-3.5 border-b border-gray-200 dark:border-gray-700"
                >
                    <UInput v-model="q" placeholder="Filter..." />
                    <UButton icon="i-heroicons-plus" color="primary" />
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
                                icon="i-heroicons-ellipsis-horizontal-20-solid"
                            />
                        </UDropdown>
                    </template>
                </UTable>
                <div
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
        {
            id: 7,
            name: "Lindsay Walton",
            title: "Front-end Developer",
            email: "lindsay-walton@example.com",
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
                click: () => console.log("Edit", row.id),
            },
            {
                label: "Delete",
                icon: "i-heroicons-trash-20-solid",
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
</script>
