import subprocess


class CPU(object):
    def getUsedCPU(self):
        proc = subprocess.Popen("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {printf usage}'", shell=True, stdout=subprocess.PIPE)

        cpu_usage = proc.communicate()
        if len(cpu_usage) > 0:
            return int(float(cpu_usage[0]))

        return 0

    def getFreeCPU(self, UsedCPU=None):
        if UsedCPU is None:
            return 100 - self.getUsedCPU()

        return 100 - UsedCPU
