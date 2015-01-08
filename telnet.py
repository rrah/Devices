#-------------------------------------------------------------------------------
# Name:        telnet
# Purpose:     Custom version of telnetlib to make my life a little easier
#
# Author:      Robert Walker
#
# Created:     09/11/2013
# Copyright:   (c) Robert Walker 2013
# Licence:     GPLv3
#-------------------------------------------------------------------------------

"""
An edited version of telnetlib to remove the opening of the port in
__init__ and to allow opening the connection without passing any parameters
to the open method"""

import telnetlib as tel
from telnetlib import DEBUGLEVEL, select


class Telnet(tel.Telnet):

    enabled = True
    connected = False

    def getHost(self):

        return self.host

    def getId(self):

        return self.id

    def getPort(self):

        return self.port

    def getName(self):

        return self.name

    def isEnabled(self):

        return self.enabled

    def isConnected(self):

        return self.connected

    def setConnected(self, state):

        if type(state) is bool:
            self.connected = state
        else:
            raise TypeError('state must be bool')

    def setEnabled(self, enable = True):

        if type(enable) == bool:
            self.enabled = enable
        else:
            raise TypeError('enable must be bool')

    def setHost(self, host):

        try:
            self.host = str(host)
        except TypeError:
            raise TypeError('Host must be stringerable')

    def setPort(self, port):

        try:
            self.port = str(port)
        except TypeError:
            raise TypeError('Port must be stringerable')

    def setName(self, name):

        self.name = name

    def close(self):

        if self.isConnected():
            tel.Telnet.close(self)
            self.setConnected(False)

    def open(self):

        """
        Open the connection, but uses the host and port already
        defined, to make my life easier."""

        if not self.isConnected():
            tel.Telnet.open(self, self.host, self.port, self.timeout)
            self.setConnected(True)

    def __init__(self, host, port = 22, timeout = 1, name = None, id = None):

        """
        Taken from telnetlib.py with the final if removed so
        the connection isn't immediately opened."""

        self.debuglevel = DEBUGLEVEL
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None
        self.rawq = ''
        self.irawq = 0
        self.cookedq = ''
        self.eof = 0
        self.iacseq = '' # Buffer for IAC sequence.
        self.sb = 0 # flag for SB and SE sequence.
        self.sbdataq = ''
        self.option_callback = None
        self._has_poll = hasattr(select, 'poll')
        self.name = name
        self.id = id


def main():
    test = Telnet('192.168.0.107', 5250)
    test.open()
    test.close()

if __name__ == '__main__':
    main()
