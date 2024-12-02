import { createRouter, createWebHistory } from 'vue-router';
import ArtistsView from '../views/ArtistsView.vue';
import ShowsView from '../views/ShowsView.vue';
import TypesView from '../views/TypesView.vue';
import IncomesView from '../views/IncomesView.vue';
import ExpensesView from '../views/ExpensesView.vue';
import Login from '../views/Login.vue';
import Logout from '../views/Logout.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "ArtistsView",
      component: ArtistsView,
    },
    {
      path: "/shows",
      name: "ShowsView",
      component: ShowsView,
    },
    {
      path: "/types",
      name: "TypesView",
      component: TypesView,
    },
    {
      path: "/incomes",
      name: "IncomesView",
      component: IncomesView,
    },
    {
      path: "/expenses",
      name: "ExpensesView",
      component: ExpensesView,
    },
    {
      path: "/login",
      name: "Login",
      component: Login,
    },
    {
      path: "/logout",
      name: "Logout",
      component: Logout,
    },
  ]
})

export default router
