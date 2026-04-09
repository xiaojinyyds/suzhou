import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import MergeGameView from '@/views/MergeGameView.vue' 
import CheckinView from '@/views/CheckinView.vue'
import ScratchView from '@/views/ScratchView.vue'
import MerchView from '@/views/MerchView.vue'
import MyView from '@/views/MyView.vue'
import PhotoView from '@/views/PhotoView.vue'
import MerchOrdersView from '@/views/MerchOrdersView.vue'
import LoginView from "@/views/LoginView.vue";
const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
     {
    path: '/',
    name: 'login',
    component: LoginView
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView
  },
  {
    path: '/merge',
    name: 'merge',
    component: MergeGameView
  },
  { path: '/checkin',
     name: 'checkin', 
     component: CheckinView },
  { path: '/scratch',
     name: 'scratch',
     component: ScratchView },
  { path: '/merch',
     name: 'merch', 
     component: MerchView },
  { path: '/my', 
     name: 'my', 
     component: MyView },   
  { path: '/photo', 
     name: 'photo', 
     component: PhotoView },
  { path: '/merch-orders',
     name: 'merchOrders',
     component: MerchOrdersView },

  ]
})

export default router