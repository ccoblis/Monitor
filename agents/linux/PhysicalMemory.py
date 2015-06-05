import re


class PhysicalMemory(object):
    def getFreeMemory(self):
        with open('/proc/meminfo', 'r') as f:
            self.meminfo = f.read()
            self.matched = re.search(r'^MemFree:\s*', self.meminfo)
            if self.matched:
                return int(self.matched.groups()[0])
        return 0

    def getTotalMemory(self):
        with open('/proc/meminfo', 'r') as f:
            self.meminfo = f.read()
            self.matched = re.search(r'^MemTotal:\s+(\d+)', self.meminfo)
            if self.matched:
                return int(self.matched.groups()[0])
        return 0

    def getUsedMemory(self, FreePhysicalMemory=None):
        if FreePhysicalMemory is None:
            return int(self.getTotalMemory()) - int(self.getFreeMemory())
        return int(self.getTotalMemory()) - int(FreePhysicalMemory)
