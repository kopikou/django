<script setup>
  import axios from "axios";
  import { computed, ref, onBeforeMount } from "vue";
  import _ from "lodash";
  import Cookies from "js-cookie";
  import { storeToRefs } from "pinia";
  import useUserProfileStore from "@/stores/userProfileStore";

  onBeforeMount(() => {
    axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
  });
  const userProfileStore = useUserProfileStore();
  const {
    is_auth,
    userId,
    is_superuser
  } = storeToRefs(userProfileStore)

  const shows = ref([]);
  const incomes = ref([]);
  const incomeToAdd = ref({});
  const incomeToEdit = ref({});
  const showIdFilter = ref(0);
  const users = ref([]);
  const userIdFilter = ref(0);

  const loading = ref(false);

  const showsById = computed(() => {
    return _.keyBy(shows.value, (x) => x.id);
  });

  async function fetchIncome() {
    const params = {};
    if (showIdFilter.value !== "Все" && showIdFilter.value !== 0) {
      params.show = showIdFilter.value;
    }
    if (userIdFilter.value !== 0 && userIdFilter.value != "Все"){
      params.user = userIdFilter.value;
    }
    
    const r = await axios.get("/api/income/",{
        params: params
      });
    loading.value = true;
    //const r = await axios.get("/api/income/");
    incomes.value = r.data;
    loading.value = false;
  }
  async function fetchShows() {
    const r = await axios.get("/api/show/");
    shows.value = r.data;
  }

  async function fetchUsers() {
    const r = await axios.get("/api/users/");
    users.value = r.data;
  }
  async function fetchUserProfile() {  
  if (is_superuser)
    fetchUsers()
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
    incomeToEdit.value = { ...income, show: income.show.id };
  }
  async function onUpdateIncome() {
    await axios.put(`/api/income/${incomeToEdit.value.id}/`, {
      ...incomeToEdit.value,
    });
    await fetchIncome();
  }

  async function onSelectClick(){
    await fetchIncome();
  }

  onBeforeMount(async () => {
    await fetchIncome();
    await fetchShows();
    await fetchUserProfile();
  });
</script>

<template>
  <div class="container" >
    <div class="p-2" >
      <form @submit.prevent.stop="onIncomeAdd" class="mb-2" v-if="is_auth">
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
            <button class="btn btn-outline-secondary">Добавить</button>
          </div>
        </div>
      </form>

      <div v-if="loading">Загрузка...</div>
      <div class="form-floating  mb-2" v-if="is_auth">
        <select class="form-select" v-model="showIdFilter" @change="onSelectClick" required>
          <option>Все</option>
          <option :value="s.id" v-for="s in shows">{{ s.name }}</option>
        </select>
        <label for="floatingInput">Шоу</label>
      </div>
      
      <div class="form-floating mb-2" v-if="is_superuser">
        <select class="form-select" v-model="userIdFilter" @change="onSelectClick" required>
          <option>Все</option>
          <option :value="u.id" v-for="u in users" >{{ u.username }}</option>
        </select>
        <label for="floatingInput">Пользователь</label>
      </div>

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

    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr auto auto;
    gap: 8px;
    align-content: center;
    align-items: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.178);
    background-color:rgba(250, 161, 235, 0.358);
  }
</style>