import threading

class Device():

    _lock = threading.RLock()

    enabled = True

    def get_name(self):

        return self.name

    def getName(self):

        DeprecationWarning
        self.get_name

    def isEnabled(self):

        return self.enabled

    def setEnabled(self, *args):

        DeprecationWarning
        self.set_enabled(*args)

    def set_enabled(self, enable = True):

        if type(enable) == bool:
            self.enabled = enable
        else:
            raise TypeError('enable must be bool')

    def getHost(self):

        return self.host

    def getPort(self):

        return self.port

    def setHost(self, *args):

        DeprecationWarning
        return self.set_host(*args)

    def setPort(self, *args):

        DeprecationWarning
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