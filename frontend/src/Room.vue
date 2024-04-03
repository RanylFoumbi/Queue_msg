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
                    <span class="font-medium text-green-600 ">{{ user.toUpperCase().substring(0,2) }}</span>
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
               <Message v-for="message in messages" :key="message.id" :message="message" />
            </div>
            
            <!-- Chat Input -->
            <footer class="bg-white border-t border-gray-300 p-4 absolute bottom-0 w-3/4">
                <div class="flex items-center">
                    <input type="text" placeholder="Entrer a message..." v-model="currentMessage" class="w-full p-2 rounded-md border border-gray-400 focus:outline-none focus:border-blue-500">
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
            messages: [
                {
                    id: '1',
                    content: 'Hey Bob, how\'s it going?',
                    createdAt: '2021-09-01T12:00:00Z',
                    isDelivered: false,
                    sender: 'Alice'
                },
                {
                    id: '2',
                    content: 'Hi Alice! I\'m good, just finished a great book. How about you?',
                    createdAt: '2021-09-01T12:01:00Z',
                    isDelivered: true,
                    sender: 'rany'
                },
                {
                    id: '3',
                    content: 'I\'m doing great too! What book did you read?',
                    createdAt: '2021-09-01T12:02:00Z',
                    isDelivered: true,
                    sender: 'Alice'
                },
                {
                    id: '4',
                    content: 'I read "The Alchemist" by Paulo Coelho. It was amazing!',
                    createdAt: '2021-09-01T12:03:00Z',
                    isDelivered: true,
                    sender: 'rany'
                },
                {
                    id: '1',
                    content: 'Hey Bob, how\'s it going?',
                    createdAt: '2021-09-01T12:00:00Z',
                    isDelivered: false,
                    sender: 'Alice7'
                },
                {
                    id: '2',
                    content: 'Hi Alice! I\'m good, just finished a great book. How about you?',
                    createdAt: '2021-09-01T12:01:00Z',
                    isDelivered: true,
                    sender: 'rany'
                },
                {
                    id: '3',
                    content: 'I\'m doing great too! What book did you read?',
                    createdAt: '2021-09-01T12:02:00Z',
                    isDelivered: true,
                    sender: 'Alice4'
                },
                {
                    id: '4',
                    content: 'I read "The Alchemist" by Paulo Coelho. It was amazing!',
                    createdAt: '2021-09-01T12:03:00Z',
                    isDelivered: true,
                    sender: 'rany'
                },
                {
                    id: '1',
                    content: 'Hey Bob, how\'s it going?',
                    createdAt: '2021-09-01T12:00:00Z',
                    isDelivered: false,
                    sender: 'Alice'
                },
                {
                    id: '2',
                    content: 'Hi Alice! I\'m good, just finished a great book. How about you?',
                    createdAt: '2021-09-01T12:01:00Z',
                    isDelivered: true,
                    sender: 'rany2'
                },
                {
                    id: '3',
                    content: 'I\'m doing great too! What book did you read?',
                    createdAt: '2021-09-01T12:02:00Z',
                    isDelivered: true,
                    sender: 'Alice3'
                },
                {
                    id: '4',
                    content: 'I read "The Alchemist" by Paulo Coelho. It was amazing!',
                    createdAt: '2021-09-01T12:03:00Z',
                    isDelivered: true,
                    sender: 'rany'
                },
                {
                    id: '3',
                    content: 'I\'m doing great too! What book did you read?',
                    createdAt: '2021-09-01T12:02:00Z',
                    isDelivered: true,
                    sender: 'Alice3'
                },
                {
                    id: '4',
                    content: 'I read "The Alchemist" by Paulo Coelho. It was amazing!',
                    createdAt: '2021-09-01T12:03:00Z',
                    isDelivered: true,
                    sender: 'rany'
                },
                {
                    id: '3',
                    content: 'I\'m doing great too! What book did you read?',
                    createdAt: '2021-09-01T12:02:00Z',
                    isDelivered: true,
                    sender: 'Alice0'
                },
                {
                    id: '4',
                    content: 'I read "The Alchemist" by Paulo Coelho. It was amazing!',
                    createdAt: '2021-09-01T12:03:00Z',
                    isDelivered: true,
                    sender: 'rany6'
                },
                {
                    id: '3',
                    content: 'I\'m doing great too! What book did you read?',
                    createdAt: '2021-09-01T12:02:00Z',
                    isDelivered: true,
                    sender: 'Alice38'
                },
                {
                    id: '4',
                    content: 'I read "The Alchemist" by Paulo Coelho. It was amazing!',
                    createdAt: '2021-09-01T12:03:00Z',
                    isDelivered: true,
                    sender: 'rany16'
                },
                {
                    id: '3',
                    content: 'I\'m doing great too! What book did you read?',
                    createdAt: '2021-09-01T12:02:00Z',
                    isDelivered: true,
                    sender: 'Alice08'
                },
                {
                    id: '4',
                    content: 'I read "The Alchemist" by Paulo Coelho. It was amazing!',
                    createdAt: '2021-09-01T12:03:00Z',
                    isDelivered: true,
                    sender: 'rany90'
                },
            ]
        }
    },
    async mounted() {
        // Get the list of users from the messages
        console.log(router.currentRoute.value.query.username);
        this.currentUsername = router.currentRoute.value.query.username as string;
        console.log(this.currentUsername);
        this.users = this.messages.map((message) => message.sender);
        this.users.push(this.currentUsername);
        this.users = this.users.reverse().filter((value, index, self) => self.indexOf(value) === index);
    },
    async created() {
        // Connect to the chat server
    },
    methods: {
        // Send a message to the chat server
        sendMessage() {
            // Send the message to the chat server
            this.messages.push({
                id: '5',
                content: this.currentMessage,
                createdAt: new Date().toISOString(),
                isDelivered: false,
                sender: String(this.currentUsername)
            });

            this.$nextTick(() => {
                const container: any = this.$refs.messagesContainer;
                container.scrollTop = container.scrollHeight;
                this.currentMessage = '';
            });

        },

        // Receive a message from the chat server
        receiveMessage() {
            // Receive the message from the chat server
        },

        logout() {
            // Disconnect from the chat server
            this.loading = true;
            setTimeout(() => {
                this.$router.push({ name: 'Login' });
                this.loading = false;
            }, 1000);
        }
    },
    watch: {
        // Watch for new messages
    }

}
</script>

<style scoped>
</style>