import socket
import threading

class EV3Socket:
    clients = []
    name = 'EV3'
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 9999
        self.server = None
        
    def start(self, SocketIO):
        # Create a socket object
        print('Starting server...')
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set the SO_REUSEADDR option
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            
            while True:
                # Establish connection with client
                client, addr = self.server.accept()
                self.clients.append(client)
                print('Got connection from', addr)
                client.send(b'Thank you for connecting')
                SocketIO.emit('ev3', {'message': 'EV3 connected'})
                # Start a new thread to handle the client
                client_thread = threading.Thread(target=self.handle_client, args=(client,SocketIO,))
                client_thread.start()
            
        except KeyboardInterrupt:
            self.close()
            
    def handle_client(self, client, SocketIO):
        while True:
            data = client.recv(1024)
            data = data.decode('utf-8')
            if not data:
                break
            if data == 'quit':
                print('Client disconnected')
                SocketIO.emit('ev3', {'message': 'EV3 disconnected'})
                self.disconnect(client)
                break
            print(data)
            client.send(b'Hello from server')
        
        self.disconnect(client)
        
    def close(self):
        if self.server:
            self.server.close()
            print('Server closed')
            
            # Close all client connections
            for client in self.clients:
                client.close()
            self.clients = []
            
    def disconnect(self, client):
        client.close()
        if client in self.clients:
            self.clients.remove(client)
        
    def send(self, message):
        for client in self.clients:
            client.send(message)



