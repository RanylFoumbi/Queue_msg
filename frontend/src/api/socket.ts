// import { DefaultEventsMap } from "@socket.io/component-emitter";
// import { io, Socket } from "socket.io-client";

class SocketioService {
  socket: WebSocket | undefined;
  constructor() {}

  setupSocketConnection(username: string) {
    this.socket = new WebSocket(`ws://localhost:80/receive/${username}`);
  }

  disconnectSocket() {
    if (this.socket) {
      this.socket.close();
    }
  }
}

export default new SocketioService();