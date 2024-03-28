<template>
    <div v-if="canRoleDo('create')">
        <div class="col-12 mb-3">
            <h4>Create Inventory</h4>
        </div>
        <div class="row mb-3">
            <div class="col">
                <label class="form-label">Name</label>
                <input type="text" class="form-control" v-model="inputProductName"/>
            </div>
            <div class="col">
                <label class="form-label">Description</label>
                <input type="text" class="form-control" v-model="inputProductDescription" />
            </div>
            <div class="col">
                <label class="form-label">Supplier</label>
                <select class="form-control" v-model="inputProductSupplierId">
                    <option v-for="supplier in suppliers" :value="supplier.id">{{ supplier.name }}</option>
                </select>
            </div>
        </div>
        <div class="row">
            <div class="d-flex justify-content-end">
                <button class="btn btn-primary" @click.prevent="addProduct">Add Product</button>
            </div>
        </div>
        <div class="mt-4 mb-4">
            <hr />
        </div>
    </div>
    <template v-if="canRoleDo('view')">
        <div class="row mb-3" >
            <div class="col-12 mb-3">
                <h4>Search Inventory</h4>
            </div>
            <div class="col-3">
                <label class="form-label">Name</label>
                <input class="form-control" type="text" @keyup.enter="fetchInventory" v-model="searchName" />
            </div>
            <div class="col-3">
                <label class="form-label">Supplier</label>
                <select class="form-control" @change="fetchInventory" v-model="searchSupplier">
                    <option value=""></option>
                    <option v-for="supplier in suppliers" :value="supplier.id">{{ supplier.name }}</option>
                </select>
            </div>
            <div class="col-3">
                <label class="form-label">Description</label>
                <input class="form-control" type="text" @keyup.enter="fetchInventory" v-model="searchDescription" />
            </div>
            <div class="col-3 d-flex justify-content-end">
                <div>
                    <label class="form-label">&nbsp;</label>
                    <div>
                        <div class="btn-group">
                            <button class="btn btn-warning" @click.prevent="resetFilter">Reset</button>
                            <button class="btn btn-success" @click.prevent="fetchInventory">Filter</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-3">
                <label class="form-label">Sort By</label>
                <select class="form-control" @change="fetchInventory" v-model="sortInventoryBy">
                    <option value=""></option>
                    <option value="Name">Name</option>
                    <option value="Description">Description</option>
                </select>
            </div>
            <div class="col-3">
                <label class="form-label">Order By</label>
                <select class="form-control" @change="fetchInventory" v-model="sortOrder">
                    <option value="asc">Ascending</option>
                    <option value="desc">Descending</option>
                </select>
            </div>
        </div>
        <div class="mt-4 mb-4">
            <hr />
        </div>
    </template>
    <div class="row mb-3">
        <div class="col-12 mb-3">
            <h4>List of Inventory</h4>
        </div>
        <div class="col-6">
            <div class="row">
                <label class="col-2 col-form-label">Per page</label>
                <div class="col-2">
                    <select class="form-control" @change="currentPage = 1; fetchInventory" v-model="perPage">
                            <option value="10">10</option>
                            <option value="50">50</option>
                            <option value="100">100</option>
                            <option value="500">500</option>
                    </select>
                </div>
                <label class="col-2 col-form-label">Go to page</label>
                <div class="col-2">
                    <select class="form-control" @change="fetchInventory" v-model="currentPage">
                        <template v-for="page in Array(totalPage).keys()">
                            <option :value="page+1">{{ page+1 }}</option>
                        </template>
                    </select>
                </div>
            </div>
        </div>
        <div class="offset-3 col d-flex justify-content-end">
            <div>
                <div>Displaying {{ currentItemsDisplay }} of {{ totalItem }} items</div>
                <div class="text-center"><a role="button" class="text-primary" @click.prevent="updatePage(-1)">Prev</a> | Page {{ currentPage }}  | <a role="button"class="text-primary" @click.prevent="updatePage(1)">Next</a></div>
            </div>
        </div>
    </div>
    <div>
        <table class="table table-hover table-bordered">
            <thead class="table-secondary">
                <tr>
                    <th class="text-start">Name</th>
                    <th class="text-start">Supplier</th>
                    <th class="text-start">Description</th>
                </tr>
            </thead>
            <tbody>
                <template v-if="products.length > 0">
                    <tr v-for="product in products">
                        <td class="text-start"><router-link :to="`/inventory/${product.id}`">{{ product.name }}</router-link></td>
                        <td class="text-start">{{ product.supplier.name }}</td>
                        <td class="text-start">{{ product.description }}</td>
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
import {ref, computed} from 'vue'
import {useRoleStore, useSupplierStore} from '../store'
import InventoryService from '../services/InventoryService'
import {storeToRefs} from 'pinia'

const products = ref<Array<any>>([])

const { suppliers } = storeToRefs(useSupplierStore())
const { canRoleDo } = useRoleStore()

const inputProductName = ref<string>('')
const inputProductDescription = ref<string>('')
const inputProductSupplierId = ref<string>('')

const searchName = ref<string>('')
const searchDescription = ref<string>('')
const searchSupplier = ref<string>('')
const sortInventoryBy = ref<string>('')
const sortOrder = ref<string>('')
const currentPage = ref<number>(1)
const perPage = ref<number>(10)
const totalPage = ref<number>(0)
const totalItem = ref<number>(0)
const currentItemsDisplay = computed<number>(() => products.value.length < perPage.value ? products.value.length : perPage.value)

const fetchInventory = async () => {
    const query: any = {}
    if (searchName.value) {
        query['search_name'] = searchName.value
    }

    if (searchDescription.value) {
        query['search_description'] = searchDescription.value
    }

    if (searchSupplier.value) {
        query['search_supplier_id'] = searchSupplier.value
    }

    if (sortInventoryBy.value) {
        query['sort_by'] = sortInventoryBy.value
    }

    if (sortOrder.value) {
        query['sort_order'] = sortOrder.value
    }

    if (perPage.value) {
        query['per_page'] = perPage.value
    }

    query['current_page'] = currentPage.value


    InventoryService.getInventories(query)
        .then(({ data }) => {
            products.value = data.data
            currentPage.value = data.currentPage
            perPage.value = data.perPage
            totalPage.value = data.totalPage
            totalItem.value = data.totalItem
        }).catch(() => {
            products.value = []
            currentPage.value = 1
            totalItem.value = 0
            totalPage.value = 1
        })
}

const addProduct = () => {
    if (inputProductName.value === '' || inputProductDescription.value === '' || inputProductSupplierId.value === '') {
        return
    }

    const data = {
        name: inputProductName.value,
        description: inputProductDescription.value,
        supplier_id: inputProductSupplierId.value,
    }

    InventoryService.addInventory(data)
        .then(() => {
            inputProductName.value = ''
            inputProductDescription.value = ''
            inputProductSupplierId.value = ''

            resetFilter()
            alert('New product added')
        })
}

const updatePage = (numOfPage: number) => {
    if (currentPage.value + numOfPage <= 0) {
        return
    }

    if (numOfPage == 1 && totalItem.value - (perPage.value * currentPage.value) <= 0) {
        return
    }

    currentPage.value += numOfPage

    fetchInventory()
}

const resetFilter = () => {
    searchName.value = ''
    searchDescription.value = ''
    searchSupplier.value = ''
    sortInventoryBy.value = ''
    sortOrder.value = ''
    currentPage.value = 1
    perPage.value = 10
    totalItem.value = 0
    totalPage.value = 1

    fetchInventory()
}

fetchInventory()

</script>
