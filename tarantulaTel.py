#-------------------------------------------------------------------------------
# Name:        tarantulaTel
# Purpose:     Wrapper for the telnet interface to tarantula
#
# Author:      Robert Walker
#
# Created:     10/11/2013
# Copyright:   (c) Robert Walker 2013
# Licence:     GPLv3
#-------------------------------------------------------------------------------


import socket
import telnet as tel
import datetime as dt
import xml.etree.cElementTree as et

from math import floor

import device

host = 'strm1.ystv.york.ac.uk'
port = 9815


NoEvent = et.fromstring('<MCEvent></MCEvent>')


class Tarantula(tel.Telnet, device.Device):

##    nextLiveId = NoEvent
    nextLiveShow = NoEvent
    currentShow = NoEvent
    nextShow = NoEvent

    def isLiveScheduled(self):

        """
        Returns True if a live show is scheduled in the next
        24 hours, False otherwise"""

        if self.nextLiveShow is not NoEvent:
            return True
        else:
            return False

    def isLive(self):

        """
        Returns True if a live show is currently in progress,
        False if otherwise."""

        try:
            if self.currentShow.find('targetdevice').text == 'LiveShow':
                return True
            else:
                return False
        except AttributeError:
            return False

    def setShowData(self, type_, element):

        if type_ == 'live':
            self.nextLiveShow = element
        elif type_ == 'current':
            self.currentShow = element
        elif type_ == 'next':
            self.nextShow = element
        else:
            raise TypeError('Unrecognised show type')

    def getShowData(self, showType, data = None):

        if showType == 'live':
            if data is None:
                return self.nextLiveShow
            else:
                try:
                    return self.nextLiveShow.find(data).text
                except AttributeError:
                    return None
        elif showType == 'current':
            if data is None:
                return self.currentShow
            else:
                try:
                    return self.currentShow.find(data).text
                except AttributeError:
                    return None
        elif showType == 'next':
            if data is None:
                return self.nextShow
            else:
                try:
                    return self.nextShow.find(data).text
                except AttributeError:
                    return None
        else:
            raise TypeError('Unrecognised show type')

    def getShowId(self, type_):

        if type_ not in ['live', 'current', 'next']:
            raise TypeError('Unrecognised show type')
        return self.getShowData(type_).find('eventid').text

    def stopLive(self):

        self.open()
        self.write('<Action><ActionType>Trigger</ActionType>' +
                    '<channel>Default</channel>' +
                    '<eventid>{}</eventid></Action>\r\n'.format(
                                                        self.getNextLiveId()))
        events = self.read_until('\r\n', 1)
        events = self.read_until('\r\n', 1)
        self.close()

    def delayLive(self, length = None, option = None):

        """
        Send the command to tarantula to delay the live show and
        play something to fill the time

        int length: time (in frames) to delay/fill
        str option: what to fill the time with (currently 'Lazy mode' or
        'Clock'.)"""

        length = int(length) * 60 * 25
        try:
            tarantula.open()
            tarantula.write('<Action><ActionType>UpdatePlaylist</Acti' +
                                'onType><channel>Default</channel><specialac' +
                                'tion>next</specialaction></Action>\r\n')
            events = tarantula.read_until('\r\n', 1)
            events = tarantula.read_until('\r\n', 1)
            if '200 SUCCESS' in events:
                events = events.strip('200 SUCCESS\r\n')
            root = et.XML(events)
            for event in root.findall('MCEvent'):
                if event.find('targetdevice').text == 'LiveShow':
                    time = event.find('time').text
                else:
                    raise NoEventError
            tarantula.write('<Action><ActionType>Shunt</ActionType>' +
                                '<channel>Default</channel>' +
                                '<starttime>{}</starttime>'.format(time) +
                                '<length>{}</length></Action>\r\n'.format(
                                                                        length))
            events = tarantula.read_until('\r\n', 1)
            if option == 'Lazy mode':
                tarantula.write('<Action><ActionType>Add</ActionType>' +
                                '<MCEvent><action>1</action>' +
                                '<channel>Default</channel>' +
                                '<duration>{}</duration>'.format(length) +
                                '<type>fixed</type><actiondata />' +
                                '<targetdevice>Lazy Scheduler</targetdevice>' +
                                '<time>{}</time>'.format(time) +
                                '<childevents /></MCEvent></Action>\r\n')
                event = tarantula.read_until('\r\n', 1)
            elif option == 'Clock':
                tarantula.write('<Action><ActionType>Add</ActionType>' +
                                '<MCEvent><action>1</action>' +
                                '<channel>Default</channel>' +
                                '<duration>{}</duration>'.format(length) +
                                '<type>fixed</type><actiondata>' +
                                '<graphicname>Clock</graphicname>' +
                                '<hostlayer>1</hostlayer></actiondata>' +
                                '<targetdevice>GFX Helper</targetdevice>' +
                                '<time>{}</time>'.format(time) +
                                '<childevents /></MCEvent></Action>\r\n')
                event = tarantula.read_until('\r\n', 1)
            else:
                pass # Shouldn't really happen...
            tarantula.close()
        except (socket.timeout, socket.socket):
            return False
        if event == '200 SUCCESS':
            return True # Woo, alls good :)
        else:
            return False
            # eh, will worry about this later

    def updateShowData(self):
        time = dt.datetime.now() + dt.timedelta(minutes = 1)
        time = time.isoformat(' ')
        self.open()
        self.write('<Action><ActionType>UpdatePlaylist</Acti' +
                        'onType><channel>Default</channel>' +
                        '<starttime>{}</starttime>'.format(time) +
                        '<length>86400</length></Action>\r\n')
        events = self.read_until('\r\n', 1)
        events = self.read_until('\r\n', 1)
        if '200 SUCCESS' in events:
            events = events.strip('200 SUCCESS\r\n')
        self.close()
        try:
            root = et.XML(events)
            for event in root.findall('MCEvent'):
                if (event.find('targetdevice').text == 'LiveShow' or
                    event.find('targetdevice').text == 'Live Show'):
                    self.setShowData('live', event)
                    break
            else:
                self.setShowData('live', NoEvent)
        except et.ParseError:
            self.setShowData('live', NoEvent)
        for type_ in ['next', 'current']:
            self.open()
            self.write('<Action><ActionType>UpdatePlaylist</Acti' +
                            'onType><channel>Default</channel><specialac' +
                            'tion>{}</specialaction></Action>\r\n'.format(
                                                                    type_))
            events = self.read_until('\r\n')
            events = self.read_until('\r\n')
            if '200 SUCCESS' in events:
                events = events.strip('200 SUCCESS\r\n')
            self.close()
            if events == '':
                self.setShowData(type_, NoEvent)
            try:
                root = et.XML(events)
                for event in root.findall('MCEvent'):
                    self.setShowData(type_, event)
                    break
                else:
                    self.setShowData(type_, NoEvent)
            except et.ParseError:
                self.setShowData(type_, NoEvent)


    def __init__(self, host = host, port = port):
        tel.Telnet.__init__(self, host = host, port = port)
        self.name = 'tarantula'


def main():
    tarantula = Tarantula()
    tarantula.updateShowData()
    print tarantula.getShowData('current', 'description')


if __name__ == '__main__':
    main()
