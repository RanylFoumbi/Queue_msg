<template>
    <div v-if="message?.content=='DISCONNECTION_MESSAGE'">
      <div class="flex items-center justify-center w-full my-7">
             <div class="flex flex-col items-center gap-1.5 p-2.5 bg-gray-100 rounded-xl">
                 <span class="text-sm font-normal text-red-400 ">{{ formatDate(message?.createdAt as string) }}</span>
                 <span class="text-sm font-normal text-gray-400 "><b class="text-black">{{ formatName(message?.sender) }}</b> a quitté la conversation</span>
             </div>
      </div>
    </div>

    <div v-else-if="message?.content=='CONNECTION_MESSAGE'">
     <div class="flex items-center justify-center w-full my-7">
          <div class="flex flex-col items-center gap-1.5 p-2.5 bg-gray-100 rounded-xl">
                <span class="text-sm font-normal text-green-400 ">{{ formatDate(message?.createdAt as string) }}</span>
                <span class="text-sm font-normal text-gray-400 "><b class="text-black">{{ formatName(message?.sender) }}</b> vient de rejoindre la conversation</span>
          </div>
     </div>
    </div>


   <div v-else :class="isMine ? 'flex justify-end' : 'w-full'">
    <div :class="isMine ? 'flex items-start flex-row-reverse gap-2.5 my-7' : 'flex items-start gap-2.5 my-9'">
        <div class="relative inline-flex items-center justify-center w-10 h-10 overflow-hidden bg-gray-100 rounded-full">
            <span class="font-medium text-green-600 ">{{ message?.sender.toUpperCase().substring(0,2) }}</span>
        </div>
        <div class="flex flex-col gap-1 w-full max-w-[320px]">
            <div :class="isMine ? 'flex items-center space-x-2 rtl:space-x-reverse justify-start' : 'flex items-center space-x-2 rtl:space-x-reverse justify-end'">
                <span class="text-sm font-normal text-gray-500 ">{{ formatDate(message?.createdAt as string) }}</span>
            </div>
            <div :class="isMine ? 'flex flex-col leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-s-xl rounded-b-xl' : 'flex flex-col leading-1.5 p-4 border-gray-200 bg-gray-300 rounded-e-xl rounded-es-xl'">
                <p class="text-sm font-normal text-gray-500 "> {{ message?.content }}</p>
            </div>
        </div>
    </div>
   </div>
</template>

<script lang="ts">
import { PropType } from 'vue';
import type { IMessage } from '../models/Message';
import router from '../router';

export default {
  name: 'Message',
    props: {
        message: Object as PropType<IMessage>,
    },
    data() {
        return {};
    },
    computed: {
        isMine() {
            const currentUser = router.currentRoute.value.params.username;
            return this.message?.sender === currentUser;
        },
    },

    methods: {
        formatDate(date: string) {
            return new Date(date).toLocaleString();
        },
        formatName(name: string) {
            if (!name) return '';
            return name.charAt(0).toUpperCase() + name.slice(1);
        },
    },
}
</script>

<style scoped></style>