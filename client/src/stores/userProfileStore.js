import axios from "axios";
import { defineStore } from "pinia";
import { onBeforeMount, ref } from "vue";

const useUserProfileStore = defineStore("UserProfileStore", {
    // const is_auth = ref();
    // const userId = ref();
    // const is_superuser = ref();

    // onBeforeMount(async()=>{
    //     const r = await axios.get("/api/user-profile/info/");
    //     is_auth.value = r.data.is_authenticated;
    //     userId.value = r.data.id;
    //     is_superuser.value = r.data.is_superuser
    // })

    state: () => ({
        is_auth: false,
        userId: '',
        is_superuser: false,
    }),
    actions: {
        updateUserInfo(r) {
            this.is_auth = r.data.is_authenticated;
            this.userId = r.data.id;
            this.is_superuser = r.data.is_superuser;
        },
        clearUserInfo() {
            this.is_auth = false;
            this.userId = '';
            this.is_superuser = false;
        },
    },

    //return{is_auth, userId, is_superuser}
})
export default useUserProfileStore;