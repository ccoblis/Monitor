from wmi import WMI


class PhysicalMemory(object):
    def __init__(self):
        self.objwmi = WMI()

    def getFreeMemory(self):
        return self.objwmi.Win32_OperatingSystem()[0].FreePhysicalMemory

    def getTotalMemory(self):
        return self.objwmi.Win32_OperatingSystem()[0].TotalVisibleMemorySize

    def getUsedMemory(self, FreePhysicalMemory=None):
        if FreePhysicalMemory is None:
            return int(self.getTotalMemory()) - int(self.getFreeMemory())
        return int(self.getTotalMemory()) - int(FreePhysicalMemory)

    def getPhysicalMemoryAgent(self):
        _physical_memory = {}

        _physical_memory['FreeMemory'] = \
                                self.getFreeMemory()
        _physical_memory['UsedMemory'] = \
                                self.getUsedMemory()
        _physical_memory['TotalMemory'] = \
                                self.getTotalMemory()

        return _physical_memory
