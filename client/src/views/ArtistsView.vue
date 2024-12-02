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
  const artists = ref([]);
  const artistToAdd = ref({});
  const artistToEdit = ref({});
  const artistsPictureRef = ref();
  const artistAddImageUrl = ref();
  const artistEditImageUrl = ref();
  const artistImageShow = ref({});
  const artistsEditPictureRef = ref();
  const showIdFilter = ref(0);
  const users = ref([]);
  const userIdFilter = ref(0);

  const loading = ref(false);

  const showsById = computed(() => {
    return _.keyBy(shows.value, (x) => x.id);
  });

  async function fetchArtists() {
    const params = {};
    if (showIdFilter.value !== "Все" && showIdFilter.value !== 0) {
      params.show = showIdFilter.value;
    }
    if (userIdFilter.value !== 0 && userIdFilter.value != "Все"){
      params.user = userIdFilter.value;
    }
    
    const r = await axios.get("/api/artists/",{
        params: params
      });
    loading.value = true;
   
    artists.value = r.data;
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

  async function onArtistAdd() {
    const formData = new FormData();
    if(artistsPictureRef.value.files[0]){
      formData.append('picture',artistsPictureRef.value.files[0])
    }  

    formData.set('name',artistToAdd.value.name)
    formData.set('show',artistToAdd.value.show)

    await axios.post("/api/artists/", formData,{
      headers:{
        'Content-Type': 'multipart/form-data'
      }
      //...artistToAdd.value,
    });
    await fetchArtists();
  }
  async function onRemoveClick(artist) {
    await axios.delete(`/api/artists/${artist.id}/`);
    await fetchArtists();
  }
  async function onArtistEditClick(artist) {
    artistToEdit.value = { ...artist, show: artist.show.id };
    artistEditImageUrl.value = artist.picture;
  }
  async function onUpdateArtist() {
    const formData = new FormData();
    if(artistsEditPictureRef.value.files[0]){
      formData.append('picture',artistsEditPictureRef.value.files[0])
    }
    //console.log(artistToEdit.value);
    
    formData.set('name',artistToEdit.value.name)
    formData.set('show',artistToEdit.value.show)
    await axios.put(`/api/artists/${artistToEdit.value.id}/`, formData,{
      headers:{
        'Content-Type': 'multipart/form-data'
      }
      //...artistToEdit.value,
    });
    await fetchArtists();
  }

  async function artistsAddPictureChange(){
    artistAddImageUrl.value = URL.createObjectURL(artistsPictureRef.value.files[0])
  }
  async function onArtistPictureClick(artist) {
    artistImageShow.value = { ...artist };
  }
  async function artistsEditPictureChange(){
    artistEditImageUrl.value = URL.createObjectURL(artistsEditPictureRef.value.files[0])
  }

  async function onSelectClick(){
    await fetchArtists();
  }

  onBeforeMount(async () => {
    await fetchArtists();
    await fetchShows();
    await fetchUserProfile();
  });
</script>

<template>
  <div class="container">
    <div class="p-2">
      <form @submit.prevent.stop="onArtistAdd" v-if="is_superuser"  class="mb-2">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="artistToAdd.name"
                required
              />
              <label for="floatingInput">Имя</label>
            </div>
          </div>
          <div class="col-auto">
            <input class="form-control" type="file" ref="artistsPictureRef" @change="artistsAddPictureChange"></input>
          </div>
          <div class="col-auto">
            <img 
              :src="artistAddImageUrl" 
              style="max-height: 60px;" 
              alt=""
              >
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <select class="form-select" v-model="artistToAdd.show" required>
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
      <div class="form-floating">
        <select class="form-select" v-model="showIdFilter" @change="onSelectClick" required>
          <option>Все</option>
          <option :value="s.id" v-for="s in shows">{{ s.name }}</option>
        </select>
        <label for="floatingInput">Шоу</label>
      </div>
      
      <!-- <div class="form-floating" v-if="is_superuser">
        <select class="form-select" v-model="userIdFilter" @change="onSelectClick" required>
          <option>Все</option>
          <option :value="u.id" v-for="u in users" >{{ u.username }}</option>
        </select>
        <label for="floatingInput">Пользователь</label>
      </div> -->

      <div>
        <div v-for="item in artists" class="artist-item">
          <div>{{ item.name }}</div>
          <div>"{{ showsById[item.show.id]?.name }}"</div>
          <div v-show="item.picture"><img 
            :src="item.picture" 
            @click="onArtistPictureClick(item)"
            style="max-height: 60px;"
            data-bs-toggle="modal"
            data-bs-target="#imageArtistModal"
            >
          </div>

          <button
            class="btn btn-success"
            @click="onArtistEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editArtistModal"
            v-if="is_superuser">
            <i class="bi bi-pen-fill"></i>
          </button>

          <button class="btn btn-danger" @click="onRemoveClick(item)" v-if="is_superuser">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editArtistModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
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
                    v-model="artistToEdit.name"
                  />
                  <label for="floatingInput">Имя</label>
                </div>
              </div>
              <div class="col-auto">
                <div class="form-floating">
                  <input class="form-control" type="file" ref="artistsEditPictureRef" @change="artistsEditPictureChange"></input>
                </div>
              </div>
              <div class="col-auto">
                <img 
                  :src="artistEditImageUrl" 
                  style="max-height: 60px;" 
                  alt=""
                >
              </div>
              <div class="col-auto">
                <div class="form-floating">
                  <select class="form-select" v-model="artistToEdit.show">
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
              @click="onUpdateArtist"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="imageArtistModal" tabindex="-1">
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
                <div v-show="artistImageShow.picture"><img :src="artistImageShow.picture" style="max-width: 100%;max-height: 100%;"></div>
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
  .artist-item {
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
