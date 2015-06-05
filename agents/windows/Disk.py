from wmi import WMI

"""
[<_wmi_object: \\computerName\root\cimv2:
    Win32_PerfRawData_PerfDisk_PhysicalDisk.Name="0 C: D:">,
<_wmi_object: \\computerName\root\cimv2:
    Win32_PerfRawData_PerfDisk_PhysicalDisk.Name="_Total">]
"""


class Disk(object):
    def __init__(self):
        self.objwmi = WMI()

    def getFreeSpace(self):
        drive = self.objwmi.Win32_LogicalDisk()

        freespace = 0
        for i in drive:
            if i.FreeSpace is not None:
                freespace += int(i.FreeSpace)
        return freespace

    def getTotalSpace(self):
        drive = self.objwmi.Win32_LogicalDisk()

        totalspace = 0
        for i in drive:
            if i.Size is not None:
                totalspace += int(i.Size)
        return totalspace

    def getUsedSpace(self, FreeSpace=None):
        if FreeSpace is None:
            return self.getTotalSpace() - self.getFreeSpace()

        return self.getTotalSpace() - FreeSpace

    def getReadUsage(self):
        return self.objwmi.Win32_PerfRawData_PerfDisk_PhysicalDisk()[1] \
            .DiskReadsPerSec

    def getWriteUsage(self):
        return self.objwmi.Win32_PerfRawData_PerfDisk_PhysicalDisk()[1] \
            .DiskWritesPerSec
