import socket

import device as dev

import copy

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

    def set_input_labels(self, labels):
        
        self.set_labels(labels, 'inputs')
        
    def set_output_labels(self, labels):
        
        self.set_labels(labels, 'outputs')
            
    def set_labels(self, labels, type_):
        
        for label in labels:
            self.pending_labels[type_][label[0]] = label

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
        try:
            self.read(2)
        except socket.timeout:
            pass # No change to routing
        self.close()

    def get_map(self):

        return self.routing

    def open(self):

        if not self.isConnected():
            self.socket = socket.create_connection((self.host, self.port))
            self.socket.settimeout(0.5)
            self.setConnected(True)

    def write(self, text):

        if type(text) == type(str):
            raise TypeError('Must be string')
        else:
            return self.socket.sendall(bytearray.fromhex(text))

    def read(self, bytes_ = 256):

        return hexlify(self.socket.recv(bytes_))
    
    def read_until(self, target = None):
        
        msg = ''
        size = len(target) / 2
        while True:
            read = self.read(size)
            if read == target:
                msg += read
                break
            else:
                msg += read
                
        return msg

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
            self.socket.shutdown(socket.SHUT_RD)
            self.socket.close()
            self.setConnected(False)


    def update(self):

        """
        Get routing information and update object connections"""

        self.open()
        self.write('c000')
        output = self.read_until('c000')
        self.close()
        self.routing = []
        for i in range(0, len(output)/6):
            self.routing.append([int(output[i * 6 + 2:i * 6 + 4], 16),
                                         int(output[i * 6 + 4:i * 6 + 6], 16)])
        
        # Check if labels are waiting to be changed
        if cmp(self.pending_labels, self.labels) is not 0:
            self.labels = copy.deepcopy(self.pending_labels)

    def __init__(self, host, port, default_labels = None):
        
        # Set the new default labels if required
        if default_labels is not None:
            self._defualt_labels = copy.deepcopy(default_labels)
        self.connected = False
        self.host = host
        self.port = int(port)
        self.name = 'vik'
        self.labels = copy.deepcopy(self._defualt_labels)
        self.pending_labels = copy.deepcopy(self._defualt_labels)
        self.routing = []



def main():
    try:
        host = 'localhost'
        port = 2004
        vik = Vikinx(host, port)
        vik.update()
        print vik.get_map()
        vik.set_map([(1, 7)])
        print 'pause'
        sleep(1)
        vik.update()
        print vik.get_map()
    except:
        vik.close()
        raise

if __name__ == '__main__':
    main()