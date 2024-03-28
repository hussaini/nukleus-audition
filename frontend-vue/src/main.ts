import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import {createRouter, createWebHistory, RouterOptions} from 'vue-router'
import InventoryIndex from './pages/InventoryIndex.vue'
import InventoryShow from './pages/InventoryShow.vue'
import RoleCreate from './pages/RoleIndex.vue'
import {createPinia} from 'pinia'

const routes = [
    { path: '/', redirect: '/inventory' },
    { path: '/inventory', component: InventoryIndex },
    { path: '/inventory/:productId', component: InventoryShow },
    { path: '/role/create', component: RoleCreate },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
} as RouterOptions)

createApp(App)
    .use(createPinia())
    .use(router)
    .mount('#app')
