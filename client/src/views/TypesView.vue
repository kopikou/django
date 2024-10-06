<script setup>
  import axios from "axios";
  import { computed, ref, onBeforeMount } from "vue";
  import _ from "lodash";
  import Cookies from "js-cookie";

  onBeforeMount(() => {
    axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
  });

  const types = ref([]);  
  const typeToAdd = ref({});
  const typeToEdit = ref({});

  const loading = ref(false);

  async function fetchTypes() {
    loading.value = true;
    const r = await axios.get("/api/type/");
    types.value = r.data;
    loading.value = false;
  }

  async function onTypeAdd() {
    await axios.post("/api/type/", {
      ...typeToAdd.value,
    });
    await fetchTypes();
  }
  async function onRemoveClick(type) {
    await axios.delete(`/api/type/${type.id}/`);
    await fetchTypes();
  }
  async function onTypeEditClick(type) {
    typeToEdit.value = { ...type };
  }
  async function onUpdateType() {
    await axios.put(`/api/type/${typeToEdit.value.id}/`, {
      ...typeToEdit.value,
    });
    await fetchTypes();
  }

  onBeforeMount(async () => {
    await fetchTypes();
  });
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onTypeAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="typeToAdd.show_type"
                required
              />
              <label for="floatingInput">Тип Шоу</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div v-if="loading">Загрузка...</div>

      <div>
        <div v-for="item in types" class="type-item">
          <div>{{ item.show_type }}</div>

          <button
            class="btn btn-success"
            @click="onTypeEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editTypeModal"
          >
            <i class="bi bi-pen-fill"></i>
          </button>

          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editTypeModal" tabindex="-1">
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
                    type="text"
                    class="form-control"
                    v-model="typeToEdit.show_type"
                  />
                  <label for="floatingInput">Тип шоу</label>
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
              @click="onUpdateType"
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
  .type-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid black;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr auto auto;
    gap: 8px;
    align-content: center;
    align-items: center;
  }
</style>