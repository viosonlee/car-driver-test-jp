import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/exam',
    name: 'Exam',
    component: () => import('../views/Exam.vue')
  },
  {
    path: '/review',
    name: 'Review',
    component: () => import('../views/Review.vue')
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
