import socket

# Create Simple Socket Client in Python 3 for EV3 Lego

class EV3Client:
    def __init__(self):
        self.host = '127.0.0.1'  # Server IP address
        self.port = 9999  # Server port number
        self.client = None
        
    def connect(self):
        try:
            # Create a socket object
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the server
            self.client.connect((self.host, self.port))

            # Receive data from the server
            while True:
                    data = self.receive()
                    if(data == b'quit' or not data):
                        print('Server disconnected')
                        self.close()
                        break
                    print(data.decode('utf-8'))
                    
                    
                

            # Close the connection
            ## self.close()

        except Exception as e:
            print('Error:', e)
            self.close()
            
        except KeyboardInterrupt:
            self.client.send(b'quit')
            self.close()
            
    
    def send(self, message):
        self.client.send(message)
        
    def receive(self):
        return self.client.recv(1024)
        
    def close(self):
        if self.client:
            self.client.close()
        
ev3_client = EV3Client()
ev3_client.connect()