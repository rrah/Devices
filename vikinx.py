import telnet as tel

host = 'localhost'
port = 2001

class vikinx(tel.Telnet):
    
    def update(self):
##        self.open()
        self.write(bytearray([1,1,0,0,0,0,0,0]))
        self.write(bytearray([1,1,0,0,0,0,0,0]))
        
    def self.write(self, bytes):
        print bytes
        
vik = vikinx()
vik.update
