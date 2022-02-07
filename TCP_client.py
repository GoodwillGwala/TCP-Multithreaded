import socket
import json



class Client():

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
        self.port = 1234
        self.sock.connect((self.host, self.port))
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
        print("Server says...")
        try:
            message = data.decode("utf-8")
        except json.JSONDecodeError:
            raise ValueError("Decode:timeout")

        print(message)
        return message


    def talkToServer(self):
         """
         sending message to server
         """


         while not self.sock._closed:
            try:
                """


                """

                data = input("Enter message to transmit: ")

                message = self.encode(data)

                self.sock.send(self.encode(data))

                if data.lower() == self.signal.lower():
                    self.sock.close()


            except self.sock.timeout:
                raise ValueError("Listen:timeout")

            if not self.sock._closed:
                self.listenToServer()


    def listenToServer(self):

        message = []
        try:

            """
            The recv method reads data on the connection,
            and address is the address bound to the socket
            on the other end of the connection.
            """

            data = self.sock.recv(4096)

        except self.sock.timeout:
            raise ValueError("listenToServer:timeout")

        self.decode(data)

if __name__ == "__main__":
    Client().talkToServer()
