import subprocess


class Disk(object):
    def __init__(self):
        self.data = self.GetSpace()

    def GetSpace(self):
        disks = []
        proc = subprocess.Popen("df", shell=True, stdout=subprocess.PIPE)
        data = proc.communicate()
        if len(data) > 0:
            data = data[0].split("\n")[1:]
            for i in data:
                if len(i.strip()) > 0:
                    x = i.split()
                    # Filesystem     1K-blocks   Used Available Use% Mounted on
                    # /dev/loop0      18761008  15246876   2554440  86% /
                    k = {
                        "filesystem":    x[0],
                        "1k-blocks":    int(x[1]),
                        "used":    int(x[2]),
                        "available":    int(x[3]),
                        "use":    x[4],
                        "mounted_on":    x[5],
                        }
                    disks.append(k)
        return disks

    def getFreeSpace(self):
        freespace = 0
        for i in self.data:
            freespace += i['available']

        return freespace

    def getUsedSpace(self):
        usedspace = 0
        for i in self.data:
            usedspace += i['used']

        return usedspace

    def getTotalSpace(self):
        return self.getFreeSpace() + self.getUsedSpace()

    def getReadUsage(self):
        return 0

    def getWriteUsage(self):
        return 0
