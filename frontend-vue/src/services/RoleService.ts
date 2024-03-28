import httpClient from './HttpClient'

export default {
    getRoles() {
        return httpClient.get('/api/roles')
    },

    createRole(data: object) {
        return httpClient.post('/api/roles/create', data)
    },

    switchRole(data: object) {
        return httpClient.post('/api/switch-role', data)
    },

    getPermissions() {
        return httpClient.get('/api/roles/permissions')
    },

    getSubjects() {
        return httpClient.get('/api/roles/subjects')
    },
}
