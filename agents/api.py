import platform
import json


class Agents(object):
    def __init__(self):
        self.opstr = platform.system().lower()
        self.cpu_instance = None
        self.physicalmemory_instance = None
        self.disk_instance = None
        self.network_instance = None

        if self.opstr == 'windows':
            from windows import CPU, PhysicalMemory, Disk, Network

            self.cpu_instance = CPU.CPU()
            self.physicalmemory_instance = PhysicalMemory.PhysicalMemory()
            self.disk_instance = Disk.Disk()
            self.network_instance = Network.Network()
        elif self.opstr == 'linux':
            from linux import CPU, PhysicalMemory, Disk, Network

            self.cpu_instance = CPU.CPU()
            self.physicalmemory_instance = PhysicalMemory.PhysicalMemory()
            self.disk_instance = Disk.Disk()
            self.network_instance = Network.Network()
        else:
            raise Exception("Unsupported operating system")

    def getAgents(self):
        self.details = {}

        self.details['CPU'] = self.getCPUAgent()
        self.details['PhysicalMemory'] = self.getPhysicalMemory()
        self.details['Disk'] = self.getDiskAgent()
        self.details['Network'] = self.getNetworkAgent()

        return self.details

    def getSerializedAgents(self):
        return json.dumps(self.getAgents())

    @staticmethod
    def getUnserializedAgents(self, json_object):
        return json.load(json_object)

    def getCPUAgent(self):
        _cpu = {}

        _cpu['UsedCPU'] = self.cpu_instance.getUsedCPU()
        _cpu['FreeCPU'] = self.cpu_instance.getFreeCPU(_cpu['UsedCPU'])

        return _cpu

    def getPhysicalMemory(self):
        _physical_memory = {}

        _physical_memory['FreeMemory'] = \
                                self.physicalmemory_instance.getFreeMemory()
        _physical_memory['UsedMemory'] = \
                                self.physicalmemory_instance.getUsedMemory()
        _physical_memory['TotalMemory'] = \
                                self.physicalmemory_instance.getTotalMemory()

        return _physical_memory

    def getDiskAgent(self):
        _disk = {}

        # _disk['ReadUsage'] = self.disk_instance.getReadUsage()
        # _disk['WriteUsage'] = self.disk_instance.getWriteUsage()

        _disk['FreeSpace'] = self.disk_instance.getFreeSpace()
        _disk['TotalSpace'] = self.disk_instance.getTotalSpace()

        return _disk

    def getNetworkAgent(self):
        _network = {}
        _network['BytesReceivedPersec'] = \
                                self.network_instance.getBytesReceivedPersec()
        _network['BytesSentPersec'] = \
                                self.network_instance.getBytesSentPersec()

        return _network
