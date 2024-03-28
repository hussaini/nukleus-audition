import {defineStore} from 'pinia'

export const useRoleStore = defineStore('roles', {
    state: () => ({
        roles: [] as Array<any>,
        currentRole: '',
        subjects: [] as Array<any>,
        permissions: [] as Array<any>,
    }),
    actions: {
        canRoleDo(action: string) {
            const role = this.roles.find(findRole => findRole.name === this.currentRole)

            if (role) {
                const permission = role.permissions.find((findPermission: any) => findPermission.action === action)
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
        suppliers: [] as Array<any>,
    }),
})
