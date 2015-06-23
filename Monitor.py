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

        for instance in db_api.get_data():
            print '============ MACHINE ID %d ============' % (instance.id)
            data = json.loads(instance.data)
            #print 'Data -> ' + str(data)
            for (agent_key, agent_value) in data.iteritems():
                print '>>> %s:' % (agent_key)
                for (key, value) in agent_value.iteritems():
                    print '%s:\t %s' % (key, value)
            print '====================================\n'
    except KeyboardInterrupt:
        exit()
    except Exception, e:
        print "Exception handled...\nDetail:\n%s" % e
