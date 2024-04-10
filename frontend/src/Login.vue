<template>
    <div class="flex h-screen flex-col justify-center items-center px-6 py-12 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <img class="mx-auto h-12 w-auto" src="https://tailwindui.com/img/logos/workflow-mark-indigo-600.svg"
                alt="Workflow">
            <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in to your
                account</h2>
        </div>

        <div class="mt-10 mx-auto md:w-[25%] w-[70%]">
            <form class="space-y-6" @submit.prevent="joinChat">
                <div>
                    <label for="username" class="block text-sm font-medium leading-6 text-gray-900">Nom
                        d'utilisateur</label>
                    <div class="mt-2">
                        <input type="text" placeholder="Entrez votre nom" v-model="username" required
                            class="w-full p-2 rounded-md border border-gray-400 focus:outline-none focus:border-blue-500">
                    </div>
                </div>

                <div>
                    <button type="submit"
                        :class="{'cursor-not-allowed opacity-50': loading}"
                        :disabled="loading"
                        class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                        <Loader v-if="loading" :state="loading"/>
                            Joindre le chat
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import Loader from './components/Loader.vue';
import router from './router';

export default {
    name: 'Login',
    components: {
        Loader,
    },
    data() {
        return {
            username: '',
            loading: false,
        };
    },
    methods: {
        async joinChat() {
            if (this.username !== '') {
                this.loading = true;
                await new Promise(resolve => setTimeout(resolve, 1000));
                router.push({ name: 'Room', params: { username: this.username }});
            }
        },
    },
}
</script>

<style scoped></style>
