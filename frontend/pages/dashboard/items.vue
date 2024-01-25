<template>
    <div>
        <UPageHeader title="Items" />
        <UPageBody>
            <div
                class="border rounded-md dark:border-gray-800 dark:bg-gray-900"
            >
                <UTable :rows="rows" :columns="columns">
                    <template #actions-data="{row}">
                        <UDropdown :items="items(row)">
                            <UButton
                                color="gray"
                                variant="ghost"
                                icon="i-heroicons-ellipsis-horizontal-20-solid"
                            />
                        </UDropdown>
                    </template>
                </UTable>
                <div
                    class="flex justify-end px-3 py-3.5 border-t dark:border-gray-800"
                >
                    <UPagination
                        v-model="page"
                        :page-count="pageCount"
                        :total="people.length"
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
    ];

    const items = (row) => [
        [
            {
                label: "Edit",
                icon: "i-heroicons-pencil-square-20-solid",
                click: () => console.log("Edit", row.id),
            },
            {
                label: "Duplicate",
                icon: "i-heroicons-document-duplicate-20-solid",
            },
        ],
        [
            {
                label: "Archive",
                icon: "i-heroicons-archive-box-20-solid",
            },
            {
                label: "Move",
                icon: "i-heroicons-arrow-right-circle-20-solid",
            },
        ],
        [
            {
                label: "Delete",
                icon: "i-heroicons-trash-20-solid",
            },
        ],
    ];

    const page = ref(1);
    const pageCount = 6;

    const rows = computed(() => {
        return people.slice(
            (page.value - 1) * pageCount,
            page.value * pageCount,
        );
    });
</script>
