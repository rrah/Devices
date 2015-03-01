#-------------------------------------------------------------------------------
# Name:        corio
# Purpose:
#
# Author:      Robert Walker
#
# Created:     17/09/2014
# Copyright:   (c) robert.walker 2014
# Licence:     GPLv3
#-------------------------------------------------------------------------------

import telnet as tel

import device

from socket import timeout

TIMEOUT = 0.5

class Corio(tel.Telnet, device.Device):

    def set_fade_speed(self, speed):

        """
        int speed = 1 - 25 set speed of fades"""
        
        with self:
            self.open()
            self.write('fade speed={}\r\n'.format(speed))
            try:
                self.read_until('>', TIMEOUT)
            except timeout:
                self.close()
                return False
            self.close()
            self._fade_speed = speed
            return True
        
    def get_fade_speed(self):
        
        return self._fade_speed

    def fade(self, in_):

        """
        fade the overlay in or out

        bool in_ = true for in, false for out"""
        with self:
            self.open()
            if in_:
                self.write('fade=1\r\n')
            else:
                self.write('fade=0\r\n')
            read = self.expect(['[>]', '[?]'], TIMEOUT)
            if read[0]:
                self.close()
                return False
            self.close()
            return True
        
    def is_faded_in(self):
        
        return self._faded_in
    
    def update(self):
        
        with self:
            self.open()
            self.write('fade\r\n')
            read = (self.expect(['[0-1]'], 1))
            self._faded_in = True if '1' in read[2] else False if '0' in read[2] else None
            self.write('fade speed\r\n')
            self._fade_speed = int(self.expect(['[0-9]{1,2}'], 1)[2])
            self.close()
        return True
        

    def __init__(self, host, port, *args, **kwargs):
        tel.Telnet.__init__(self, host, port, *args, **kwargs)
        
    def fade_in(self):
        
        return self.fade(True)
        
    def fade_out(self):
        
        return self.fade(False)


def main():
    cor = Corio('localhost', 2003)
    print cor.get_fade_speed()

if __name__ == '__main__':
    main()
