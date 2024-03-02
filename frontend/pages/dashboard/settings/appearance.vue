<template>
    <UDashboardPanelContent class="pb-24">
        <UDashboardSection
            title="Theme"
            description="Customize the look and feel of your dashboard."
        >
            <template #links>
                <UColorModeSelect color="gray" />
            </template>
        </UDashboardSection>
    </UDashboardPanelContent>
</template>

<script setup lang="ts"></script>
