<script setup>
  import { storeToRefs } from "pinia";
  import useUserProfileStore from "@/stores/userProfileStore";
  import { computed, ref, onBeforeMount } from "vue";
  import Cookies from "js-cookie";
  import axios from 'axios';
  onBeforeMount(() => {
    axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
  });
  const userProfileStore = useUserProfileStore();

  onBeforeMount(async () => {
    await axios.get('/api/user-profile/logout/');

    userProfileStore.clearUserInfo();
  });
</script>

<template>
  <div class="container">
    <div class="row justify-content-md-center p-2">Спасибо за посещение нашего сайта!</div>
    <div><a class="row justify-content-md-center p-2" href="/login">Войти</a></div>
  </div>
</template>

<style lang="scss" scoped></style>