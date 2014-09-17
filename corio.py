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


    def checkResponse(self, response):

        """
        See if the response is actually a good one or not"""

        if response == '>':
            return True
        else:
            return False

    def fadeSpeed(self, speed):

        """
        int speed = 1 - 25 set speed of fades"""

        self.open()
        self.write('fade speed={}'.format(speed))
        response = self.read_until('>', 0.1)
        self.close()
        if self.checkResponse(response):
            return True
        else:
            return False

    def fade(self, in_):

        """
        fade the overlay in or out

        bool in_ = true for in, false for out"""

        self.open()
        if in_:
            self.write('fade=1')
        else:
            self.write('fade=0')
        sleep(0.1)
        response = self.read_until('>', 0.1)
        self.close()
        if self.checkResponse(response):
            return True
        else:
            return False

    def __init__(self, host, port, *args, **kwargs):
        tel.Telnet.__init__(self, host, port, *args, **kwargs)



def main():
    pass

if __name__ == '__main__':
    main()
