<script setup>
  import axios from "axios";
  import { computed, ref, onBeforeMount } from "vue";
  import _ from "lodash";
  import Cookies from "js-cookie";

  onBeforeMount(() => {
    axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
  });

  const types = ref([]);  
  const shows = ref([]);
  const showToAdd = ref({});
  const showToEdit = ref({});
  const showsPictureRef = ref();
  const showAddImageUrl = ref();
  const showEditImageUrl = ref();
  const showImageShow = ref({});
  const showsPictureRef1 = ref();

  const loading = ref(false);

  const typesById = computed(() => {
    return _.keyBy(types.value, (x) => x.id);
  });

  async function fetchShows() {
    loading.value = true;
    const r = await axios.get("/api/show/");
    shows.value = r.data;
    loading.value = false;
  }
  async function fetchTypes() {
    const r = await axios.get("/api/type/");
    types.value = r.data;
  }

  async function onShowAdd() {
    const formData = new FormData();
    if(showsPictureRef.value.files[0]){
      formData.append('picture',showsPictureRef.value.files[0])
    }  

    formData.set('name',showToAdd.value.name)
    formData.set('type',showToAdd.value.type)
    formData.set('price',showToAdd.value.price)

    await axios.post("/api/show/", formData,{
      headers:{
        'Content-Type': 'multipart/form-data'
      }
    });
    //await axios.post("/api/show/", {
    //  ...showToAdd.value,
    //});
    await fetchShows();
  }
  async function onRemoveClick(show) {
    await axios.delete(`/api/show/${show.id}/`);
    await fetchShows();
  }
  async function onShowEditClick(show) {
    showToEdit.value = { ...show, type: show.type.id };
    showEditImageUrl.value = show.picture;
  }
  async function onUpdateShow() {
    const formData = new FormData();
    if(showsPictureRef1.value.files[0]){
      formData.append('picture',showsPictureRef1.value.files[0])
    }

    formData.set('name',showToEdit.value.name)
    formData.set('type',showToEdit.value.type)
    formData.set('price',showToEdit.value.price)

    await axios.put(`/api/show/${showToEdit.value.id}/`, formData,{
      headers:{
        'Content-Type': 'multipart/form-data'
      }
      //...artistToEdit.value,
    });
    //await axios.put(`/api/show/${showToEdit.value.id}/`, {
    //  ...showToEdit.value,
    //});
    await fetchShows();
  }

  async function showsAddPictureChange(){
    showAddImageUrl.value = URL.createObjectURL(showsPictureRef.value.files[0])
  }
  async function onShowPictureClick(show) {
    showImageShow.value = { ...show };
  }
  async function showsEditPictureChange(){
    showEditImageUrl.value = URL.createObjectURL(showsPictureRef1.value.files[0])
  }

  onBeforeMount(async () => {
    await fetchShows();
    await fetchTypes();
  });
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onShowAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="showToAdd.name"
                required
              />
              <label for="floatingInput">Название</label>
            </div>
          </div>
          <div class="col-auto">
            <input class="form-control" type="file" ref="showsPictureRef" @change="showsAddPictureChange"></input>
          </div>
          <div class="col-auto">
            <img 
              :src="showAddImageUrl" 
              style="max-height: 60px;" 
              alt=""
              >
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <select class="form-select" v-model="showToAdd.type" required>
                <option :value="t.id" v-for="t in types">{{ t.show_type }}</option>
              </select>
              <label for="floatingInput">Тип шоу</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <input
                type="number"
                class="form-control"
                v-model="showToAdd.price"
                required
              />
              <label for="floatingInput">Стоимость</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div v-if="loading">Загрузка...</div>

      <div>
        <div v-for="item in shows" class="show-item">
          <div>{{ item.name }}</div>
          <div>{{ typesById[item.type.id]?.show_type }}</div>
          <div>{{ item.price }}</div>
          <div v-show="item.picture"><img 
            :src="item.picture" 
            @click="onShowPictureClick(item)"
            style="max-height: 60px;"
            data-bs-toggle="modal"
            data-bs-target="#imageShowModal"
            >
          </div>

          <button
            class="btn btn-success"
            @click="onShowEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editShowModal"
          >
            <i class="bi bi-pen-fill"></i>
          </button>

          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editShowModal" tabindex="-1">
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
                    v-model="showToEdit.name"
                  />
                  <label for="floatingInput">Название</label>
                </div>
              </div>
              <div class="col-auto">
                <div class="form-floating">
                  <input class="form-control" type="file" ref="showsPictureRef1" @change="showsEditPictureChange"></input>
                </div>
              </div>
              <div class="col-auto">
                <img 
                  :src="showEditImageUrl" 
                  style="max-height: 60px;" 
                  alt=""
                >
              </div>
              <div class="col-auto">
                <div class="form-floating">
                  <select class="form-select" v-model="showToEdit.type">
                    <option :value="t.id" v-for="t in types">
                      {{ t.show_type }}
                    </option>
                  </select>
                  <label for="floatingInput">Типы шоу</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input
                    type="number"
                    class="form-control"
                    v-model="showToEdit.price"
                  />
                  <label for="floatingInput">Стоимость</label>
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
              @click="onUpdateShow"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="imageShowModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Просмотр
            </h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
                <div v-show="showImageShow.picture"><img :src="showImageShow.picture" style="max-width: 100%;max-height: 100%;"></div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Закрыть
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
  .show-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid black;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr auto auto;
    gap: 8px;
    align-content: center;
    align-items: center;
  }
</style>
