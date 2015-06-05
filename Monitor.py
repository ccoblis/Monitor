import json
from db import api as db_api

if __name__ == "__main__":
    try:
        print 'Initializing monitor app...'
        print 'Reading from database:'
        db_data = db_api.get_data()

        if len(db_data) < 1:
            print '0 rows found! Try later!'
            exit()

        print '{0: <10} | {1: <19} | {2: <32} | {3: <16} | {4: <16}' \
              .format('ID', 'CPU Usage', 'Physical Memory Usage',
                      'Disk Usage', 'Network Usage')

        for instance in db_api.get_data():
            data = json.loads(instance.data)
            # print 'Data -> ' + str(data)
            cpu = data['CPU']
            phmem = data['PhysicalMemory']
            disk = data['Disk']
            network = data['Network']

            usage_mem = 0
            if phmem['TotalMemory'] != 0:
                usage_mem = 100 - int(int(phmem['FreeMemory']) * 100 /
                            int(phmem['TotalMemory']))

            used_disk = 0
            if disk['TotalSpace'] != 0:
                used_disk = 100 - int(int(disk['FreeSpace']) * 100 /
                            int(disk['TotalSpace']))

            print r'{0: <10} | {1:>2}% used ({2}% free) | {3}mb / {4}mb ({5}% used) | {6} / {7} ({8}% used) | {9} r - {10} s' \
              .format(instance.id, cpu['UsedCPU'], cpu['FreeCPU'],
                phmem['FreeMemory'], phmem['TotalMemory'], usage_mem,
                disk['FreeSpace'], disk['TotalSpace'], used_disk,
                network['BytesReceivedPersec'], network['BytesSentPersec'])
    except KeyboardInterrupt:
        exit()
    except Exception, e:
        print "Exception handled...\nDetail:\n%s" % e
