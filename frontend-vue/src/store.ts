import {defineStore} from 'pinia'

export const useRoleStore = defineStore('roles', {
    state: () => ({
        roles: [],
        currentRole: '',
        subjects: [],
        permissions: [],
    }),
    actions: {
        canRoleDo(action: string) {
            const role = this.roles.find(findRole => findRole.name === this.currentRole)

            if (role) {
                const permission = role.permissions.find(findPermission => findPermission.action === action)
                if (permission) {
                    return true
                }
            }

            return false
        },
    }
})

export const useSupplierStore = defineStore('suppliers', {
    state: () => ({
        suppliers: [],
    }),
})
