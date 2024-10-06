<script setup>
  import axios from "axios";
  import { computed, ref, onBeforeMount } from "vue";
  import _ from "lodash";
  import Cookies from "js-cookie";

  onBeforeMount(() => {
    axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
  });

  const shows = ref([]);
  const artists = ref([]);
  const artistToAdd = ref({});
  const artistToEdit = ref({});

  const loading = ref(false);

  const showsById = computed(() => {
    return _.keyBy(shows.value, (x) => x.id);
  });

  async function fetchArtists() {
    loading.value = true;
    const r = await axios.get("/api/artists/");
    artists.value = r.data;
    loading.value = false;
  }
  async function fetchShows() {
    const r = await axios.get("/api/show/");
    shows.value = r.data;
  }

  async function onArtistAdd() {
    await axios.post("/api/artists/", {
      ...artistToAdd.value,
    });
    await fetchArtists();
  }
  async function onRemoveClick(artist) {
    await axios.delete(`/api/artists/${artist.id}/`);
    await fetchArtists();
  }
  async function onArtistEditClick(artist) {
    artistToEdit.value = { ...artist };
  }
  async function onUpdateArtist() {
    await axios.put(`/api/artists/${artistToEdit.value.id}/`, {
      ...artistToEdit.value,
    });
    await fetchArtists();
  }

  onBeforeMount(async () => {
    await fetchArtists();
    await fetchShows();
  });
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onArtistAdd">
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
            <div class="form-floating">
              <select class="form-select" v-model="artistToAdd.show" required>
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
        <div v-for="item in artists" class="artist-item">
          <div>{{ item.name }}</div>
          <div>"{{ showsById[item.show.id]?.name }}"</div>

          <button
            class="btn btn-success"
            @click="onArtistEditClick(item)"
            data-bs-toggle="modal"
            data-bs-target="#editArtistModal"
          >
            <i class="bi bi-pen-fill"></i>
          </button>

          <button class="btn btn-danger" @click="onRemoveClick(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editArtistModal" tabindex="-1">
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
                    v-model="artistToEdit.name"
                  />
                  <label for="floatingInput">Имя</label>
                </div>
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
  </div>
</template>

<style lang="scss" scoped>
  .artist-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid black;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr 1fr auto auto;
    gap: 8px;
    align-content: center;
    align-items: center;
  }
</style>
