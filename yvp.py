#-------------------------------------------------------------------------------
# Name:        yvp
# Purpose:     Python bindings for YSTV Vision Protocol
#
# Author:      Robert Walker
#
# Created:
# Copyright:   (c) Robert 2014
# Licence:     GPLv3
#-------------------------------------------------------------------------------


import telnet as tel
import xml.etree.cElementTree as et

from time import sleep


class YVP(tel.Telnet):

    def update(self):
        self.open()
        self.read_until('\r\n', 0.2)
        if self.name == 'tally':
            self.write('<stat>\n')
            stat = self.read_until('\r\n', 1)
            stat = stat.lstrip('<stat>')
        else:
            self.write(bytearray('<stat>'))
            stat = self.read_until('\r\n', 1)
        self.close()
        if '<badc>' in stat:
            return None
        if stat is not type(et.Element):
            if stat is None or stat == '\r\n':
                return None
            try:
                stat = et.fromstring(stat)
            except et.ParseError:
                raise TypeError('Must be an xml element')
        if stat.tag == 'map':
            map = stat
        elif element.findall('map') is None:
            map = stat.findall('map')[0]
        else:
            raise ValueError('No map element found')
        links = []
        for link in map.findall('link'):
            link = link.text.split(',')
            link = (int(link[0]), int(link[1]))
            links. append(link)
        self.map = links

    def getMap(self):

        return self.map

    def __init__(self, host, port):
        tel.Telnet.__init__(self, host, port)
        self.map = []

    def link(self, in_, out):

        """
        Link the in connection to the out connection"""

        try:
            int(in_)
            int(out)
        except TypeError:
            raise TypeError('in_ and out must be int')
        msg = '<{:02}{:02}>'.format(in_, out)
        if self.name == 'tally':
            msg += '\r'
        self.open()
        sleep(0.1)
        self.write(bytearray(msg))
        self.read_until('\r\n', 0.2)
        self.close()

class Tally(YVP):

    def getConfig(self):
        return self.config

    def setConfig(self, in_, out):
        self.config[in_] = out

    def __init__(self, host, port):
        YVP.__init__(self, host, port)
        self.name = 'tally'
        self.config = [0,0,0,0,0,0]


class Mux(YVP):

    def kick(self):

        """
        Kick the mux if it's not doing things"""

        self.update()
        for link in self.getMap():
            self.link(link[0], link[1])
        self.update()

    def __init__(self, host, port):
        YVP.__init__(self, host, port)
        self.name = 'mux'

def main():
    dev = Mux('ob.dyn.ystv.york.ac.uk', 2000)
    dev.update()
    print dev.getMap()

if __name__ == '__main__':
    main()