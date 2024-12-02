<script setup>
  import { storeToRefs } from "pinia";
  import useUserProfileStore from "@/stores/userProfileStore";

  const userProfileStore = useUserProfileStore();
    const {
      is_auth,
      userId,
      is_superuser
    } = storeToRefs(userProfileStore)
    
</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Lumos</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Артисты</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/shows">Шоу</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/types">Типы шоу</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/incomes">Доходы</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/expenses">Расходы</router-link>
            </li>
          </ul>

          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Пользователь
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="/logout" v-if="is_auth">Выйти</a>
                  <a class="dropdown-item" href="/login" v-else>Войти</a>
                </li>
              
                <li><a class="dropdown-item" href="/admin">Админка</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>

  <div>
    <router-view/>
  </div>
</template>

<style lang="scss" scoped></style>
