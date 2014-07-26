import socket

from binascii import hexlify

from time import sleep

class vikinx():

    routing = []

    def open(self):

        self.socket = socket.create_connection((self.host, self.port))

    def write(self, text):

        print type(text), type('')
        if type(text) == type(str):
            raise TypeError('Must be string')
        else:
            self.socket.send(bytearray.fromhex(text))

    def read(self):

        return hexlify(self.socket.recv(100))

    def close(self):

        self.socket.close()

    def update(self):

        """
        Get routing information and update object connections"""

        self.open()
        self.write('c000')
        sleep(0.1)
        output = self.read()
        print type(output)
        self.close()
        self.routing = []
        for i in range(0, len(output)/6):
            self.routing.append([int(output[i * 6 + 4:i * 6 + 6], 16),
                            int(output[i * 6 + 2:i * 6 + 4], 16)])
        print self.routing

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.name = 'vik'



def main():
    host = '192.168.0.105'
    port = 2001
    vik = vikinx(host, port)
    vik.update()

if __name__ == '__main__':
    main()