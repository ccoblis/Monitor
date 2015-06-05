from wmi import WMI


class CPU(object):
    def __init__(self):
        self.cpu_wmi = WMI()

    def getUsedCPU(self):
        return self.cpu_wmi.Win32_Processor()[0].LoadPercentage

    def getFreeCPU(self, UsedCPU=None):
        if UsedCPU is None:
            return 100 - self.getUsedCPU()

        return 100 - UsedCPU
