import httpClient from './HttpClient'

export default {
    getInventories(queryData = {}) {
        const query = new URLSearchParams(queryData).toString()
        return httpClient.get(`/api/inventory?${query}`)
    },

    getInventoryByProductId(id: number) {
        return httpClient.get(`/api/inventory/${id}`)
    },

    addInventory(data: object) {
        return httpClient.post('/api/add-inventory', data)
    },

    updateInventory(data: object) {
        return httpClient.post('/api/update-inventory', data)
    },

    deleteInventory(data: object) {
        return httpClient.post('/api/delete-inventory', data)
    },

    getSuppliers() {
        return httpClient.get(`/api/inventory/suppliers`)
    },
}
