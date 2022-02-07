import socket
import json

class Server():

    def __init__(self):

        #Create INET, Streaming TCP socket
        #AF_INET refers to the address family ipv4
        #SOCK_STREAM provides connection oriented TCP protocol
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #set socket option to reuse address
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #A server has a bind() method which binds it to a specific IP
        #and port so that it can listen to incoming requests on that IP and PORT.

        self.host = "localhost"
        self.port = 65435
        self.sock.bind((self.host, self.port))
        self.signal = "Stop"


    def encode(self,data):
        """
        function to encode data to utf-8 format

        """
        try:
            message = data.encode()
        except json.JSONEncodeError:
            raise ValueError("Encode:timeout")
        return message

    def decode(self,data):
        """
        function to decode data to utf-8 format
        """
        print("Client says...")
        try:
            message = data.decode("utf-8")

        except json.JSONDecodeError:
            raise ValueError("Decode:timeout")

        print(message)
        return message


    def listen(self):
         """
         socket.listen(backlog)
         Listen for connections made to the socket.
         The backlog argument specifies the maximum number of
         queued connections and should be at least 0;
         the maximum value is system-dependent (usually 5)
         """
         print("Listening...")
         self.sock.listen(5)

         try:
             """
             The accept method initiates a connection with the client.
             accept return value is a pair (connection, address)
             where connection is a new socket object to send and
             receive data on the connection, and address is the address
             bound to the socket on the other end of the connection.

             """
             connection, address = self.sock.accept()

         except socket.timeout:
            raise ValueError("Listen:timeout")


         print("Connection to",address[0])

         while not self.sock._closed:
            self.listenToClient(connection, address)


    def listenToClient(self, connection, address):

        message = []
        if not self.sock._closed:
            try:

                """
                The recv method reads data on the connection,
                and address is the address bound to the socket
                on the other end of the connection.
                """
                data = connection.recv(4096)
                self.echoToClient(connection,data)

            except socket.timeout:
                raise ValueError("listenToClient:timeout")


    def echoToClient(self, connection, data):
        """
        sending message to server
        """
        data_str = self.decode(data)
        if data_str.lower() == self.signal.lower():
            self.sock.close()
        else:
            print("Echo to client...")
            connection.send(data)



if __name__ == "__main__":
    Server().listen()
