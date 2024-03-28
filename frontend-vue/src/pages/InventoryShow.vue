<template>
    <template v-if="product && (canRoleDo('view') || canRoleDo('update') || canRoleDo('delete'))">
        <div v-if="canRoleDo('view')">
            <div class="row mb-3">
                <label class="col-3">Name</label>
                <input type="text" class="col form-control" v-model="product.name">
            </div>
            <div class="row mb-3">
                <label class="col-3">Description</label>
                <input type="text" class="col form-control" v-model="product.description">
            </div>
            <div class="row mb-3">
                <label class="col-3">Supplier</label>
                <select class="col form-control" v-model="product.supplier_id">
                    <option v-for="supplier in suppliers" :value="supplier.id">{{ supplier.name }}</option>
                </select>
            </div>
            <div class="d-flex justify-content-end">
                <div class="btn-group">
                    <button v-if="canRoleDo('update')" class="btn btn-primary" @click.prevent="updateProduct">Update</button>
                    <button v-if="canRoleDo('delete')" class="btn btn-danger" @click.prevent="deleteProduct">Delete</button>
                </div>
            </div>
        </div>
    </template>
</template>

<script setup lang="ts">
import {useRoute, useRouter} from 'vue-router'
import InventoryService from '../services/InventoryService'
import {ref} from 'vue'
import { useRoleStore } from '../store'
import { useSupplierStore } from '../store'
import {storeToRefs} from 'pinia'

const route = useRoute()
const router = useRouter()
const { canRoleDo } = useRoleStore()
const { suppliers } = storeToRefs(useSupplierStore())

const productId = parseInt(route.params.productId.toString())
const product = ref<any>()

const fetchSuppliers = () => {
    InventoryService.getSuppliers()
        .then(({ data }) => {
            suppliers.value = data
        })
}

const fetchInventoryById = () => {
    InventoryService.getInventoryByProductId(productId)
        .then(({ data }) => {
            product.value = data
        }).catch(({ response: { data: { message }, status }}) => {
            let alertMessage = message
            if (status === 404) {
                alertMessage = message
            }

            alert(alertMessage)
        })
}

const updateProduct = () => {
    const data = {
        product_id: productId,
        name: product.value.name,
        description: product.value.description,
        supplier_id: product.value.supplier_id,
    }

    InventoryService.updateInventory(data)
        .then(({ data }) => {
            product.value = data
            alert('Product updated')
        }).catch(() => {
            alert('Error while updating product')
        })

}

const deleteProduct = () => {
    const isConfirmDelete = confirm('Are sure want to delete this product?')

    if (isConfirmDelete) {
        const data = {
            product_id: productId,
        }

        InventoryService.deleteInventory(data)
            .then(() => {
                router.push({ path: '/inventory' })
            }).catch(() => {
                alert('Error while deleting product')
            })
    }
}

fetchSuppliers()
fetchInventoryById()

</script>
