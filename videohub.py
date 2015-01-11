#-------------------------------------------------------------------------------
# Name:        videohub
# Purpose:     Wrapper for the videohub ethernet api
#
# Author:      Robert Walker
#
# Created:     08/11/2013
# Copyright:   (c) Robert Walker 2013
# Licence:     GPLv3
#-------------------------------------------------------------------------------

"""
Module to connect to a videohub over ethernet. Should work with any
Videohub, not just our micro"""

import logging

import device

import telnet as tel

from time import sleep

host = 'localhost'
port = '9991'


class DetailError(Exception):
    pass


class Videohub(tel.Telnet, device.Device):

    """
    Videohub object to provide a wrapper around the ethernet interface
    along with telnet stuff."""

    inputLabels = []
    outputLabels = []

    def set_map(self, map_):

        """
        list map_ : routing changes to make in form of (input, output)
        Make the relevant routing changes."""

        msg = 'VIDEO OUTPUT ROUTING:\n'
        for link in map_:
            msg += '{} {}\n'.format(link[1], link[0])
        msg += '\n'

        self.open()

        # Get all the send data
        read = self.read_until('\n\n')
        read = self.read_until('\n\n')
        read = self.read_until('\n\n')
        read = self.read_until('\n\n')
        read = self.read_until('\n\n')
        read = self.read_until('\n\n')

        # Then send ours
        self.write(msg)
        read = self.read_until('\n\n')
        if read.strip() == 'ACK':
            logging.debug('Message Acknowledged')
        else:
            logging.warning('Message not acknowledged')

        self.close()

    def setConnection(self, in_, out):

        """
        Send the connections to make to the router"""

        self.open()
        # Don't know why this needs to be here, but doesn't work without
        read = self.read_until('\n\n')
        print read
        self.write('video output routing:\n{} {}\n\n'.format(out, in_))
        self.close()

    def setDetails(self, block):

        """
        Set the details of the connected hub. Should
        only be called from within __init__ as nothing
        here should change after that"""

        block = block.split('\n')
        block = block[1:]
        self.details = dict()
        for part in block:
            part = part.split(': ')
            self.details[part[0]] = part[1]


    def setLabels(self, labels, type_):

        if type_ == 'in':
            message = 'input labels:\n'
        elif type_ == 'out':
            message = 'output labels:\n'
        else:
            raise TypeError('Unknow label type')
        for label in labels:
            message += ('{} {}\n'.format(label[0], label[1]))
        message += '\n'
        self.open()
        self.write(message)
        self.update()
        self.close()


    def getDetails(self, detail = None):
        if detail is None:
            return self.details
        try:
            return self.details[detail]
        except KeyError:
            if detail == 'outputs':
                return self.details['Video outputs']
            elif detail == 'inputs':
                return self.details['Video inputs']
            elif detail == 'id':
                return self.details['Unique ID']
            elif detail == 'model':
                return self.details['Model Name']
            else:
                try:
                    return self.details[detail]
                except KeyError:
                    raise DetailError('Unknown detail')

    def get_map(self):

        return self.getConnections()

    def getConnections(self):

        try:
            return self.connections
        except AttributeError:
            return []

    def getInputLabels(self):

        DeprecationWarning
        return self.get_input_labels()

    def get_input_labels(self):

        """
        return the labels currently set for the inputs"""

        return self.inputLabels

    def getName(self):

		return self.name

    def getOutputLabels(self):

        DeprecationWarning
        return self.get_output_labels()

    def get_output_labels(self):

        """
        return the labels currently set for the outputs"""

        try:
            return self.outputLabels
        except AttributeError:
            return []

    def recieveConnections(self, block):

        """
        Sync object connections with hub connections"""

        block = block.split('\n')
        block = block[1:]
        self.connections = []
        for part in block:
            self.connections.append(part.split(' ', 1))

    def recieveOutputLabels(self, block):

        """
        Sync object output label list with hub's list"""

        block = block.split('\n')
        block = block[1:]
        self.outputLabels = []
        for part in block:
            self.outputLabels.append(part.split(' ', 1))

    def recieveInputLabels(self, block):

        """
        Sync object input label list with hub's list"""

        block = block.split('\n')
        block = block[1:]
        self.inputLabels = []
        for part in block:
            self.inputLabels.append(part.split(' ', 1))

    def update(self, firstRun = False):

        """
        Update all the information this object holds
        on the hub."""

        self.open()
        text = self.read_until('\r\n', 0.5)
        self.close()
        text = text.split('\n\n')
        for block in text:
            if not hasattr(self, 'details') and 'VIDEOHUB DEVICE' in block:
                self.setDetails(block)
            elif 'INPUT LABELS' in block:
                self.recieveInputLabels(block)
            elif 'OUTPUT LABELS' in block:
                self.recieveOutputLabels(block)
            elif 'VIDEO OUTPUT ROUTING' in block:
                self.recieveConnections(block)

    def __init__(self, host = None, port = None):

        """
        Set up the connection to the videohub and get
        all the details"""

        tel.Telnet.__init__(self, host = host, port = port)
        self.name = 'hub'



def main():
    hub = Videohub(host, port)
    hub.update(True)
    print hub.getConnections()

if __name__ == '__main__':
    main()
