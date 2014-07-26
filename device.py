class Device():

    enabled = True
    
    def getName(self):

        return self.name

    def isEnabled(self):

        return self.enabled
       
    def setEnabled(self, enable = True):

        if type(enable) == bool:
            self.enabled = enable
        else:
            raise TypeError('enable must be bool')

    def getHost(self):
    
        return self.host
        
    def getPort(self):
    
        return self.port
        
    def setHost(self, host):
        
        self.host = host
    
    def setPort(self, port):
    
        self.port = port