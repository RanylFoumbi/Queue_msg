class SocketioService {
  socket: WebSocket | undefined;
  constructor() {}

  setupSocketConnection(username: string) {
    console.log(`Connecting to websocket...`);
    this.socket = new WebSocket(`ws://localhost:80/receive/${username}`);
    this.socket.onmessage = () => {
      console.log(`Connected to websocket.`);
    }
  }

  disconnectSocket() {
    if (this.socket) {
      this.socket.close();
    }
  }
}

export default new SocketioService();