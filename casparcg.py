#-------------------------------------------------------------------------------
# Name:        CasparCG
# Purpose:     Wrapper for CasparCG
#
# Author:      Robert Walker
#
# Created:
# Copyright:   (c) Robert Walker 2014
# Licence:
#-------------------------------------------------------------------------------

import device

import telnet as tel

from time import sleep

host = '192.168.0.107'
port = '5250'


class Casparcg(tel.Telnet, device.Device):

    def update(self):

        pass

    def runTemplate(self, template, channel = 1, layer = 20, flayer = 1, f0 = None):

        self.open()
        sleep(0.01)
        cmd = "CG {}-{} ADD {} \"{}\" 1 \"<templateData><componentData id=\\\"f0\\\"><data id=\\\"text\\\" value=\\\"{}\\\"/></componentData></templateData>\"\r\n".format(channel, layer, flayer, template, f0)
        self.write(cmd)
        sleep(0.01)
        self.close()

    def stop(self, channel, layer, flayer):

        self.open()
        sleep(0.01)
        self.write('CG {}-{} STOP {}\r\n'.format(channel, layer, flayer))
        sleep(0.01)
        self.close()

    def clear(self, channel, layer):

        self.open()
        sleep(0.01)
        self.write('CG {}-{} CLEAR\r\n'.format(channel, layer))
        sleep(0.01)
        self.close()

    def __init__(self, host = None, port = None):
        tel.Telnet.__init__(self, host = host, port = port)
        self.name = 'casparcg'

def main():
    caspar = Casparcg(host, port)
    caspar.runTemplate("WOODSTOCK2014THIRDS", f0 = "Test")
    sleep(5)
    caspar.stop(1, 20, 1)

if __name__ == '__main__':
    main()
