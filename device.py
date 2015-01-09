import threading

class Device():

    _lock = threading.RLock()

    enabled = True
    name = None

    def get_name(self):

        """
        Get the name of the device.
        By default this is None"""

        return self.name

    def getName(self):

        raise DeprecationWarning
        return self.get_name()

    def isEnabled(self):

        raise DeprecationWarning
        return self.enabled

    def setEnabled(self, *args):

        raise DeprecationWarning
        self.set_enabled(*args)

    def is_enabled(self):

        self.enabled

    def set_enabled(self, enable = True):

        if type(enable) == bool:
            self.enabled = enable
        else:
            raise TypeError('enable must be bool')

    def getHost(self):

        raise DeprecationWarning
        return self.host

    def getPort(self):

        raise DeprecationWarning
        return self.port

    def get_host(self):

        return self.host

    def get_port(self):

        return self.port

    def setHost(self, *args):

        raise DeprecationWarning
        return self.set_host(*args)

    def setPort(self, *args):

        raise DeprecationWarning
        return self.set_port(*args)

    def set_host(self, host):

        self.host = host

    def set_port(self, port):

        self.port = port

    def acquire(self):

        self._lock.acquire()

    def release(self):

        self._lock.release()

    def __enter__(self):

        self.acquire()

    def __exit__(self, type, value, traceback):

        self.release()