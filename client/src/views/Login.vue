<script setup>
  import { storeToRefs } from "pinia";
  import useUserProfileStore from "@/stores/userProfileStore";
  import { computed, ref, onBeforeMount } from "vue";
  import axios from 'axios';
  const userProfileStore = useUserProfileStore();
  const {
    is_auth,
    userId,
    is_superuser
  } = storeToRefs(userProfileStore)

  const userToLogin = ref({});
  //const is_auth= ref(false);
  async function onLogin(){
    const formData = new FormData();  

    formData.set('username',userToLogin.value.username)
    formData.set('password',userToLogin.value.password)

    const r = await axios.post("/api/user-profile/login/", formData,{
      headers:{
        'Content-Type': 'multipart/form-data'
      }
    });

    //is_auth.value = r.data.is_auth;
    if(r.data.is_auth){
      const resp = await axios.get('/api/user-profile/info/');
      userProfileStore.updateUserInfo(resp);
    }

  }
  
</script>

<template>
  <div class="container">
    <div class="p-2">
      <form @submit.prevent.stop="onLogin"  v-if="is_auth == false">
        <div class="row justify-content-md-center">
          <div data-mdb-input-init class="col-3 form-outline mb-4">
            <input type="text" id="form2Example1" class="form-control" v-model="userToLogin.username" required/>
            <label class="form-label" for="form2Example1">Имя</label>
          </div>
        </div>

        <div class="row justify-content-md-center">
          <div data-mdb-input-init class="col-3 form-outline mb-4">
            <input type="password" id="form2Example2" class="form-control" v-model="userToLogin.password" required/>
            <label class="form-label" for="form2Example2">Пароль</label>
          </div>
        </div>
        <div class="row justify-content-md-center">
          <button class="btn btn-primary btn-block mb-4 col-md-auto">Войти</button>
        </div>
        
      </form>
    </div>
    <div class="row justify-content-md-center p-2" v-if="is_auth">Вы успешно вошли!</div>
  </div>
</template>

<style lang="scss" scoped></style>
