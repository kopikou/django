import { createRouter, createWebHistory } from 'vue-router';
import ArtistsView from '../views/ArtistsView.vue';
import ShowsView from '../views/ShowsView.vue';
import TypesView from '../views/TypesView.vue';
import IncomesView from '../views/IncomesView.vue';
import ExpensesView from '../views/ExpensesView.vue';

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
  ]
})

export default router
