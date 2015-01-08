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

from time import sleep

class Corio(tel.Telnet):

    def fadeSpeed(self, speed):

        """
        int speed = 1 - 25 set speed of fades"""

        self.open()
        self.write('fade speed={}\r\n'.format(speed))
        self.close()

    def fade(self, in_):

        """
        fade the overlay in or out

        bool in_ = true for in, false for out"""

        self.open()
        if in_:
            self.write('fade=1\r\n')
        else:
            self.write('fade=0\r\n')
        self.close()

    def __init__(self, host, port, *args, **kwargs):
        tel.Telnet.__init__(self, host, port, *args, **kwargs)



def main():
    cor = Corio('localhost', 2000)
    cor.fadeSpeed(5)
    cor.fade(True)
    sleep(10)
    cor.fade(False)

if __name__ == '__main__':
    main()
