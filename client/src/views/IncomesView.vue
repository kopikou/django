<script setup>
  import axios from "axios";
  import { computed, ref, onBeforeMount } from "vue";
  import _ from "lodash";
  import Cookies from "js-cookie";

  onBeforeMount(() => {
    axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
  });

  const shows = ref([]);
  const incomes = ref([]);
  const incomeToAdd = ref({});
  const incomeToEdit = ref({});

  const loading = ref(false);

  const showsById = computed(() => {
    return _.keyBy(shows.value, (x) => x.id);
  });

  async function fetchIncome() {
    loading.value = true;
    const r = await axios.get("/api/income/");
    incomes.value = r.data;
    loading.value = false;
  }
  async function fetchShows() {
    const r = await axios.get("/api/show/");
    shows.value = r.data;
  }

  async function onIncomeAdd() {
    await axios.post("/api/income/", {
      ...incomeToAdd.value,
    });
    await fetchIncome();
  }
  async function onRemoveClick(income) {
    await axios.delete(`/api/income/${income.id}/`);
    await fetchIncome();
  }
  async function onIncomeEditClick(income) {
    incomeToEdit.value = { ...income };
  }
  async function onUpdateIncome() {
    await axios.put(`/api/income/${incomeToEdit.value.id}/`, {
      ...incomeToEdit.value,
    });
    await fetchIncome();
  }

  onBeforeMount(async () => {
    await fetchIncome();
    await fetchShows();
  });
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onIncomeAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input
                type="date"
                class="form-control"
                v-model="incomeToAdd.date"
                required
              />
              <label for="floatingInput">Дата выстпления</label>
            </div>
          </div>  
          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="incomeToAdd.place"
                required
              />
              <label for="floatingInput">Место выстпления</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <select class="form-select" v-model="incomeToAdd.show" required>
                <option :value="s.id" v-for="s in shows">{{ s.name }}</option>
              </select>
              <label for="floatingInput">Шоу</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div v-if="loading">Загрузка...</div>

      <div>
        <div v-for="item in incomes" class="income-item">
          <div>{{ item.date }}</div>
          <div>{{ item.place }}</div>
          <div>"{{ showsById[item.show.id]?.name }}"</div>

          <button
            class="btn btn-success"
            @click="onIncomeEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editIncomeModal"
          >
            <i class="bi bi-pen-fill"></i>
          </button>

          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editIncomeModal" tabindex="-1">
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
                    type="date"
                    class="form-control"
                    v-model="incomeToEdit.date"
                  />
                  <label for="floatingInput">Дата выстпления</label>
                </div>
              </div>  
              <div class="col">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="incomeToEdit.place"
                  />
                  <label for="floatingInput">Место выстпления</label>
                </div>
              </div>
              <div class="col-auto">
                <div class="form-floating">
                  <select class="form-select" v-model="incomeToEdit.show">
                    <option :value="s.id" v-for="s in shows">
                      {{ s.name }}
                    </option>
                  </select>
                  <label for="floatingInput">Шоу</label>
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
              @click="onUpdateIncome"
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
  .income-item {
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