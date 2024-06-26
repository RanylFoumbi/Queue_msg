<template>
    <div class="flex h-screen overflow-hidden">
        <!-- Sidebar -->
        <div class="w-1/4 flex flex-col justify-start bg-white border-r border-gray-300">
          <!-- Sidebar Header -->
          <header class="p-4 border-b border-gray-300 flex justify-between items-center bg-indigo-600 text-white">
            <h1 class="text-md font-semibold">Utilisateurs connectés</h1>
          </header>
        
          <!-- Contact List -->
          <div class="overflow-y-auto h-screen p-3 mb-9 pb-20">
            <div class="flex items-center mb-4 cursor-pointer bg-gray-100 p-2 rounded-md " v-for="user in users">
                <div class="relative inline-flex items-center justify-center w-10 h-10 overflow-hidden bg-gray-200 rounded-full">
                    <span class="font-medium text-green-600 ">{{ user?.toUpperCase().substring(0,2) }}</span>
                </div>
              <div class="flex-1 pl-5">
                <h2 class="text-lg font-semibold">{{ user }}</h2> 
              </div>
            </div>
          </div>
          <footer class="bg-white border-t w-full border-gray-300 flex justify-center p-4 bottom-0">
            <button @click="logout" class="bg-indigo-500 text-white px-4 py-2 rounded-md w-full">
                <Loader v-if="loading" :state="loading"/>
                Se déconnecter
            </button>
          </footer>
        </div>
        
        <!-- Main Chat Area -->
        <div class="flex-1">
            <!-- Chat Header -->
            <header class="bg-indigo-300 p-4 text-gray-700">
                <h1 class="text-md font-semibold">Chat Room</h1>
            </header>
            
            <!-- Chat Messages -->
            <div class="h-screen overflow-y-auto p-4 pb-36" ref="messagesContainer" >
               <Message v-for="(message, index) in messages" :key="index" :message="message" />
            </div>
            
            <!-- Chat Input -->
            <footer class="bg-white border-t border-gray-300 p-4 absolute bottom-0 w-3/4">
                <div class="flex items-center">
                    <input type="text" placeholder="Entrer a message..." v-model="currentMessage" @keyup.enter="sendMessage" class="w-full p-2 rounded-md border border-gray-400 focus:outline-none focus:border-blue-500">
                    <button @click="sendMessage" class="bg-indigo-500 text-white px-4 py-2 rounded-md ml-2">Envoyer</button>
                </div>
            </footer>
        </div>
    </div>
</template>

<script lang="ts">
import Message  from './components/Message.vue'
import router from './router';
import Loader from './components/Loader.vue';
import axios from 'axios';
import { IMessage } from './models/Message';

export default {
    name: 'Room',
    components: {
        Message,
        Loader
    },
    data() {
        return {
            currentUsername: null as string | null,
            users:[] as string[],
            loading: false,
            currentMessage: '', 
            socket: null as any,
            messages: [] as IMessage[],
            api_url: 'http://localhost:80'
        }
    },
    async mounted() {
         // Connect to the chat server
        this.currentUsername = router.currentRoute.value.params.username as string;
        this.socket = new WebSocket(`ws://localhost:80/receive/${this.currentUsername}`);
        axios.post(`${this.api_url}/send`, {
            content: "CONNECTION_MESSAGE",
            user_name: this.currentUsername
        });

        this.socket.onmessage = this.receiveMessage;  
    },
    methods: {
        sendMessage() {
            // Send the message to the chat server
            axios.post(`${this.api_url}/send`, {
                content: this.currentMessage,
                user_name: this.currentUsername
            });

            this.$nextTick(() => {
                const container: any = this.$refs.messagesContainer;
                container.scrollTop = container.scrollHeight;
                this.currentMessage = '';
            })

        },

        getActiveUsers() {
            // Get the list of active users from the chat server
            axios.get(`${this.api_url}/users`)
            .then((response) => {
                this.users = response.data.users;
            });
        },

        // Receive a message from the chat server
        receiveMessage(event: any) {
             const data = JSON.parse(event.data);
             console.log({data});
               this.messages.push({
                content: data.content,
                createdAt: data.sent_at,
                sender: data.user_name
            });
            this.getActiveUsers();
        },

        logout() {
            // Disconnect from the chat server
            this.loading = true;
            setTimeout(() => {
                this.$router.push({ name: 'Login' });
                this.loading = false;
                axios.post(`${this.api_url}/send`, {
                    content: 'DISCONNECTION_MESSAGE',
                    user_name: this.currentUsername
                });
            }, 1000);
        }
    },  

}
</script>

<style scoped>
</style>