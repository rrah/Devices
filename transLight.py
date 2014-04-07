#-------------------------------------------------------------------------------
# Name:        transLight
# Purpose:     Transmission Light module thingy
#
# Author:      Robert Walker
#
# Created:     15/11/2013
# Copyright:   (c) Robert Walker 2013
# Licence:
#-------------------------------------------------------------------------------

import telnet as tel
from time import sleep

host = 'localhost'
port = 2004

class TransmissionLight(tel.Telnet):

    t = False
    r = False

    def getTStatus(self):

        return self.t

    def getRStatus(self):

        return self.r

    def getLightState(self):

        if self.host is not None:
            self.open()
            self.write('s')
            state = self.read_until('\r\n', 0.1)
            self.close()

            state = state.split('\r\n')
            state = state[0]
            if state == 't':
                self.t = True
                self.r = False
            elif state == 'r':
                self.r = True
                self.t = False
            elif state == 'o':
                self.r = False
                self.t = False
            elif state =='b':
                self.r = True
                self.t = True

    def setTransmissionLight(self, light, state = None):

        """
        string light: single char string of either r or t
                        to signify which light to change

        bool state: True for on, False for off"""

        if light == 't':
            lightBool = self.t
        elif light == 'r':
            lightBool = self.r
        else:
            return 'Unrecognised light'

        if state == None:
            state = not lightBool

        if lightBool == state:
            return False

        self.open()
        if state and not self.t and not self.r:
            self.write(light)
        elif state and (not self.t or not self.r):
            self.write('b')
        elif not state and (self.t != self.r):
            self.write('o')
        elif (self.t or self.r):
            if light == 't':
                self.write('r')
            elif light == 'r':
                self.write('t')
        self.getLightState()
        self.close()

    def setRehearsalLight(self, state):

        pass

    def update(self):

        self.getLightState()

    def __init__(self, host, port):
        tel.Telnet.__init__(self, host, port)
        self.setName('trans')


def main():
    trans = TransmissionLight(host, port)
    trans.update()
    print trans.getRStatus()
    trans.setTransmissionLight('t', True)
    print trans.getRStatus()
    trans.setTransmissionLight('r', True)
    print trans.getRStatus()
    trans.setTransmissionLight('t', False)
    print trans.getRStatus()
    trans.setTransmissionLight('r', False)
    print trans.getRStatus()



if __name__ == '__main__':
    main()
