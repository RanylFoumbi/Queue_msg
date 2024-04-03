import { createRouter, createWebHistory } from 'vue-router'
import Login from '../Login.vue'
import Room from '../Room.vue'


const routes: any = [ 
    { path: '/:pathMatch(.*)*', component: Login },
    { path: '/', name: 'Login', component: Login },
    { path: '/room/:username?', name: 'Room', component: Room },
]


const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router