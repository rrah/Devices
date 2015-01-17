import socket

import device as dev

from binascii import hexlify

from time import sleep


class Vikinx(dev.Device):

    _defualt_labels={'inputs':[(0, 'Cam 1 Prime'), (1, 'Cam 1 Sec'), (2, 'Cam 2 Prime'),
                            (3, 'Cam 2 Sec'), (4, 'Cam 3 Prime'), (5, 'Cam 3 Sec'),
                            (6, 'Cam 4 Prime'), (7, 'Cam 4 Sec'), (8, 'Cam 5 Prime'),
                            (9, 'Cam 5 Sec'), (10, 'Cam 6 Prime'), (11, 'Cam 6 Sec'),
                            (12, 'VT'), (13, 'DaVE Prog'), (14, 'GFX Prog'), (15, 'Multiview')],
                'outputs':[(0, 'Dave 1'), (1, 'Dave 2'), (2, 'Dave 3'), (3, 'Dave 4'), (4, 'Multi 1'),
                            (5, 'Multi 2'), (6, 'Multi 3'), (7, 'Multi 4'), (8, 'Multi 5'),
                            (9, 'Multi 6'), (10, 'Multi 7'), (11, 'Multi 8'), (12, 'Clean feed'),
                            (13, 'Multi Patch'), (14, 'Corio'), (15, 'Dirty feed')]}
    routing = []
    connected = False

    def get_full_name(self):

        return 'Vikinx'

    def get_input_labels(self):

        return self.labels['inputs']

    def get_output_labels(self):

        return self.labels['outputs']

    def setConnection(self, *args):

        self.link(*args)

    def set_map(self, map_):

        for link in map_:
            self.link(int(link[0]), int(link[1]))

    def link(self, in_, out):

        in_ = format(in_, '02x')
        out = format(out, '02x')
        string = 'a0{}{}'.format(out, in_)
        self.open()
        self.write(string)
        sleep(0.1)
        self.read(2)
        self.close()

    def get_map(self):

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

    def read(self, bytes = 256):

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
        sleep(0.4)
        output = self.read()
        self.close()
        self.routing = []
        for i in range(0, len(output)/6):
            self.routing.append([int(output[i * 6 + 2:i * 6 + 4], 16),
                                         int(output[i * 6 + 4:i * 6 + 6], 16)])

    def __init__(self, host, port):

        self.host = host
        self.port = int(port)
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