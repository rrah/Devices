import telnet as tel
from binascii import hexlify as binhex

host = 'localhost'
port = 2001

class vikinx(tel.Telnet):
    
    def update(self):
        
        """
        Get routing information and update object connections"""
        
        self.open()
        self.write(bytearray.fromhex('c000'))
        output = binhex(self.read_until('c000'))
        self.close()
        
        output = output.split['a0']
        for out in output:
            out = [out[0:2], out[2, 4]]
        print output
        
        
vik = vikinx()
vik.update
