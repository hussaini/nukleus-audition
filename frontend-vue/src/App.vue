<template>
    <nav class="d-flex justify-content-between py-3 mb-3">
        <div>
            <router-link to="/inventory">Home</router-link>
        </div>
        <div>
            Role:
            <template v-for="role in roles">
                <span role="button" class="text-primary" :class="currentRole === role.name ? 'fw-bold' : ''" @click="switchRole(role.name)">{{ role.name }}</span>&nbsp;|&nbsp;
            </template>
            <router-link to="/role/create">New Role</router-link>
        </div>
    </nav>
    <router-view />
</template>

<script setup lang="ts">
import RoleService from './services/RoleService'
import {useRoleStore, useSupplierStore} from './store'
import {storeToRefs} from 'pinia'
import {useCookies} from 'vue3-cookies'
import InventoryService from './services/InventoryService'

const {roles, currentRole, permissions, subjects} = storeToRefs(useRoleStore())
const {suppliers} = storeToRefs(useSupplierStore())
const {cookies} =  useCookies()

const switchRole = (role: string) => {
    const data = { role }
    RoleService.switchRole(data)
        .then(() => {
            currentRole.value = cookies.get('user_role')

        })
}

const initApp = () => {
    RoleService.getRoles()
        .then(({ data }) => {
            roles.value = data
            currentRole.value = cookies.get('user_role')
        })

    RoleService.getPermissions()
        .then(({ data }) => {
            permissions.value = data
        })

    RoleService.getSubjects()
        .then(({ data }) => {
            subjects.value = data
        })

    InventoryService.getSuppliers()
        .then(({ data }) => {
            suppliers.value = data
        })

}

initApp()

</script>
