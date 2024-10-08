<script setup>
  import axios from "axios";
  import { computed, ref, onBeforeMount } from "vue";
  import _ from "lodash";
  import Cookies from "js-cookie";

  onBeforeMount(() => {
    axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
  });

  const artists = ref([]);
  const incomes = ref([]);
  const expenses = ref([]);
  const expenseToAdd = ref({});
  const expenseToEdit = ref({});

  const loading = ref(false);

  const artistsById = computed(() => {
    return _.keyBy(artists.value, (x) => x.id);
  });
  const incomesById = computed(() => {
    return _.keyBy(incomes.value, (x) => x.id);
  });

  async function fetchExpenses() {
    loading.value = true;
    const r = await axios.get("/api/expense/");
    expenses.value = r.data;
    loading.value = false;
  }
  async function fetchArtists() {
    const r = await axios.get("/api/artists/");
    artists.value = r.data;
  }
  async function fetchIncomes() {
    const r = await axios.get("/api/income/");
    incomes.value = r.data;
  }

  async function onExpenseAdd() {
    await axios.post("/api/expense/", {
      ...expenseToAdd.value,
    });
    await fetchExpenses();
  }
  async function onRemoveClick(expense) {
    await axios.delete(`/api/expense/${expense.id}/`);
    await fetchExpenses();
  }
  async function onExpenseEditClick(expense) {
    expenseToEdit.value = { ...expense, artist: expense.artist.id, income: expense.income.id };
  }
  async function onUpdateExpense() {
    await axios.put(`/api/expense/${expenseToEdit.value.id}/`, {
      ...expenseToEdit.value,
    });
    await fetchExpenses();
  }

  onBeforeMount(async () => {
    await fetchExpenses();
    await fetchArtists();
    await fetchIncomes();
  });
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onExpenseAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input
                type="number"
                class="form-control"
                v-model="expenseToAdd.salary"
                required
              />
              <label for="floatingInput">Зарплата</label>
            </div>
          </div>  
          <div class="col">
            <div class="form-floating">
              <select class="form-select" v-model="expenseToAdd.artist" required>
                <option :value="a.id" v-for="a in artists">{{ a.name }}</option>
              </select>
              <label for="floatingInput">Артист</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <select class="form-select" v-model="expenseToAdd.income" required>
                <option :value="i.id" v-for="i in incomes">{{ i.id }}</option>
              </select>
              <label for="floatingInput">ID дохода</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div v-if="loading">Загрузка...</div>

      <div>
        <div v-for="item in expenses" class="expense-item">
          <div>{{ item.salary }}</div>
          <div>{{ artistsById[item.artist.id]?.name }}</div>
          <div>"{{ incomesById[item.income.id]?.id }}"</div>

          <button
            class="btn btn-success"
            @click="onExpenseEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editExpenseModal"
          >
            <i class="bi bi-pen-fill"></i>
          </button>

          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editExpenseModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Редактировать
            </h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input
                    type="number"
                    class="form-control"
                    v-model="expenseToEdit.salary"
                  />
                  <label for="floatingInput">Зарплата</label>
                </div>
              </div>  
              <div class="col-auto">
                <div class="form-floating">
                  <select class="form-select" v-model="expenseToEdit.artist">
                    <option :value="a.id" v-for="a in artists">
                      {{ a.name }}
                    </option>
                  </select>
                  <label for="floatingInput">Артист</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <select class="form-select" v-model="expenseToEdit.income">
                    <option :value="i.id" v-for="i in incomes">
                      {{ i.id }}
                    </option>
                  </select>
                  <label for="floatingInput">ID дохода</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Закрыть
            </button>
            <button
              data-bs-dismiss="modal"
              type="button"
              class="btn btn-primary"
              @click="onUpdateExpense"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .expense-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid black;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr auto auto;
    gap: 8px;
    align-content: center;
    align-items: center;
  }
</style>