import socket

import device as dev

from binascii import hexlify

from time import sleep

class Vikinx(dev.Device):

    routing = []
    connected = False
    
    def setConnection(self, *args):
        
        self.link(*args)
    
    def link(self, in_, out):
    
        in_ = format(in_, '02x')
        out = format(out, '02x')
        string = 'a0{}{}'.format(out, in_)
        self.open()
        self.write(string)
        sleep(0.1)
        self.read(2)
        self.close()

    def getMap(self):
    
        return self.routing
    
    def open(self):

        if not self.isConnected():
            self.socket = socket.create_connection((self.host, self.port))
            self.setConnected(True)

    def write(self, text):

        if type(text) == type(str):
            raise TypeError('Must be string')
        else:
            self.socket.send(bytearray.fromhex(text))

    def read(self, bytes = 100):

        return hexlify(self.socket.recv(bytes))
        
    def isConnected(self):
    
        if self.connected:
            return True
        else:
            return False

    def setConnected(self, state):

        if type(state) is bool:
            self.connected = state
        else:
            raise TypeError('state must be bool')
            
    def close(self):
        
        if self.isConnected():
            self.socket.close()
            self.setConnected(False)
            

    def update(self):

        """
        Get routing information and update object connections"""

        self.open()
        self.write('c000')
        sleep(0.1)
        output = self.read()
        self.close()
        self.routing = []
        for i in range(0, len(output)/6):
            self.routing.append([int(output[i * 6 + 4:i * 6 + 6], 16),
                            int(output[i * 6 + 2:i * 6 + 4], 16)])

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.name = 'vik'



def main():
    host = '192.168.0.105'
    port = 2001
    vik = Vikinx(host, port)
    vik.update()
    print vik.getMap()

if __name__ == '__main__':
    main()