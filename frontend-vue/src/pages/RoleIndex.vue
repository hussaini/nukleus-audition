<template>
    <div class="mb-3">
        <div class="row mb-3">
            <label class="col-3">Role Name</label>
            <input type="text" class="col form-control" v-model="roleName">
        </div>
        <div class="row mb-3">
            <label class="col-3">Subject</label>
            <select class="col form-control" v-model="selectedSubject">
                <option v-for="subject in subjects" :value="subject.name">{{ subject.name }}</option>
            </select>
        </div>
        <div class="row mb-3">
            <label class="col-3">Permission</label>
            <div class="col" v-for="permission in permissionsBySubject">
                <div class="form-check">
                    <input type="checkbox" class="form-check-input" :value="permission.id" v-model.number="selectedPermissions">
                    <label class="form-check-label">{{ permission.action }}</label>
                </div>
            </div>
        </div>
        <div class="d-flex justify-content-end">
            <div class="btn-group">
                <button class="btn btn-primary" @click.prevent="createRole">Create Role</button>
            </div>
        </div>
    </div>
    <div>
        <table class="table table-hover table-bordered">
            <thead class="table-secondary">
                <tr>
                    <th class="text-start">Name</th>
                    <th class="text-start">Permissions</th>
                </tr>
            </thead>
            <tbody>
                <template v-if="roles.length > 0">
                    <tr v-for="role in roles">
                        <td class="text-start"><router-link :to="`/roles/${role.id}`">{{ role.name }}</router-link></td>
                        <td class="text-start">
                            <ul>
                                <li v-for="permission in role.permissions">{{ permission.action }} {{ permission.subject }}</li>
                            </ul>
                        </td>
                    </tr>
                </template>
                <template v-else>
                     <tr>
                        <td class="text-center" colspan="3">No data to displayed</td>
                    </tr>
                </template>
            </tbody>
        </table>
    </div>
</template>

<script setup lang="ts">

import {storeToRefs} from 'pinia'
import {useRoleStore} from '../store'
import {computed, ref} from 'vue'
import RoleService from '../services/RoleService'
import {useCookies} from 'vue3-cookies'

const {roles, permissions, subjects, currentRole} = storeToRefs(useRoleStore())
const {cookies} =  useCookies()

const permissionsBySubject = computed<Array<any>>(() => {
    return permissions.value.filter(findPermission => findPermission.subject === selectedSubject.value)
})

const roleName = ref<string>('')
const selectedSubject = ref<string>('')
const selectedPermissions = ref<Array<number>>([])

const createRole = (() => {
    if (roleName.value === '' || selectedSubject.value === '' || selectedPermissions.value.length === 0) {
        return
    }

    const data = {
        name: roleName.value,
        subject: selectedSubject.value,
        permissions: selectedPermissions.value,
    }

    RoleService.createRole(data)
        .then(() => {
            fetchRoles()
        })
})

const fetchRoles = (() => {
    RoleService.getRoles()
        .then(({ data }) => {
            roles.value = data
            currentRole.value = cookies.get('user_role')
        })
})

fetchRoles()

</script>
