import socket

import device as dev

from binascii import hexlify

from time import sleep


class Vikinx(dev.Device):

    _defualt_labels={'inputs':['Cam 1 Prime', 'Cam 1 Sec', 'Cam 2 Prime',
                            'Cam 2 Sec', 'Cam 3 Prime', 'Cam 3 Sec',
                            'Cam 4 Prime', 'Cam 4 Sec', 'Cam 5 Prime',
                            'Cam 5 Sec', 'Cam 6 Prime', 'Cam 6 Sec',
                            'VT', 'DaVE Prog', 'GFX Prog', 'Multiview'],
                'outputs':['Dave 1', 'Dave 2', 'Dave 3', 'Dave 4', 'Multi 1',
                            'Multi 2', 'Multi 3', 'Multi 4', 'Multi 5',
                            'Multi 6', 'Multi 7', 'Multi 8', 'Clean feed',
                            'Multi Patch', 'Corio', 'Dirty feed']}
    routing = []
    connected = False

    def get_input_labels(self):

        return self.labels['inputs']

    def get_output_labels(self):

        return self.labels['outputs']

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
        self.labels = self._defualt_labels



def main():
    host = '192.168.0.105'
    port = 2001
    vik = Vikinx(host, port)
    vik.update()
    print vik.getMap()

if __name__ == '__main__':
    main()