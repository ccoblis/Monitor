class Network(object):
    def __init__(self):
        self.data = self.GetNetworkInterfaces()

    # Credit: https://gist.github.com/racerxdl/d4b4670d189ad579ae1a
    def GetNetworkInterfaces(self):
        ifaces = []
        f = open("/proc/net/dev")
        data = f.read()
        f.close()
        data = data.split("\n")[2:]
        for i in data:
            if len(i.strip()) > 0:
                x = i.split()
                # Interface |                        Receive                          |                         Transmit
                #   iface   | bytes packets errs drop fifo frame compressed multicast | bytes packets errs drop fifo frame compressed multicast
                k = {
                    "interface":   x[0][:len(x[0])-1],
                    "tx": {
                        "bytes":   int(x[1]),
                        "packets":   int(x[2]),
                        "errs":   int(x[3]),
                        "drop":   int(x[4]),
                        "fifo":   int(x[5]),
                        "frame":   int(x[6]),
                        "compressed":   int(x[7]),
                        "multicast":   int(x[8])
                    },
                    "rx":   {
                        "bytes":   int(x[9]),
                        "packets":   int(x[10]),
                        "errs":   int(x[11]),
                        "drop":   int(x[12]),
                        "fifo":   int(x[13]),
                        "frame":   int(x[14]),
                        "compressed":   int(x[15]),
                        "multicast":   int(x[16])
                    }
                }
                ifaces.append(k)
        return ifaces

    def getBytesReceivedPersec(self):
        rx = 0
        for eth in self.data:
            rx += eth['rx']['bytes']

        return rx

    def getBytesSentPersec(self):
        tx = 0
        for eth in self.data:
            tx += eth['tx']['bytes']

        return tx

    def getNetworkAgent(self):
        _network = {}
        _network['BytesReceivedPersec'] = \
                                self.getBytesReceivedPersec()
        _network['BytesSentPersec'] = \
                                self.getBytesSentPersec()

        return _network
