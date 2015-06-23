from wmi import WMI


class Network(object):
    def __init__(self):
        self.objwmi = WMI()

    def getBytesReceivedPersec(self):
        return self.objwmi.Win32_PerfRawData_Tcpip_NetworkInterface()[0] \
            .BytesReceivedPersec

    def getBytesSentPersec(self):
        return self.objwmi.Win32_PerfRawData_Tcpip_NetworkInterface()[0] \
            .BytesSentPersec

    def getNetworkAgent(self):
        _network = {}
        _network['BytesReceivedPersec'] = \
                                self.getBytesReceivedPersec()
        _network['BytesSentPersec'] = \
                                self.getBytesSentPersec()

        return _network
