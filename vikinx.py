# import telnet as tel
import socket
from binascii import hexlify
from time import sleep

host = '192.168.0.100'
port = 2001

class vikinx():

    def open(self):
    
        self.socket = socket.create_connection((host, port))
        
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
        routing = []
        for i in range(0, len(output)/6):
            routing.append([output[i * 6 + 2:i * 6 + 4], 
                            output[i * 6 + 4:i * 6 + 6]])
        print routing
        
    def __init__(self, host, port):
    
        self.host = host
        self.port = port
        
        
vik = vikinx(host, port)
vik.update()


# vik = soc.create_connection((host, port))
# vik.send(bytearray.fromhex('c000'))
# sleep(0.1)
# output = vik.recv(100)
# print hexlify(output)