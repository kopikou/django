import axios from "axios";
import { defineStore } from "pinia";
import { onBeforeMount, ref } from "vue";

const useUserProfileStore = defineStore("UserProfileStore", ()=>{
    const is_auth = ref();
    const userId = ref();
    const is_superuser = ref();

    onBeforeMount(async()=>{
        const r = await axios.get("/api/user-profile/info/");
        is_auth.value = r.data.is_authenticated;
        userId.value = r.data.id;
        is_superuser.value = r.data.is_superuser
    })
    return{is_auth, userId, is_superuser}
})
export default useUserProfileStore;