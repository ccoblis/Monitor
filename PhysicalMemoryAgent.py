from agents.Agent import AgentRunner
from agents.windows import PhysicalMemory as WindowsPhysicalMemoryAgent
from agents.linux import PhysicalMemory as LinuxPhysicalMemoryAgent
import ConfigParser
import platform
import uuid


if __name__ == "__main__":
    try:
        opstr = platform.system().lower()
        if opstr == 'windows':
            mypmem = WindowsPhysicalMemoryAgent.PhysicalMemory()
        elif opstr == 'linux':
            mypmem = LinuxPhysicalMemoryAgent.PhysicalMemory()
        else:
            raise Exception("Unsupported operating system")

        Config = ConfigParser.ConfigParser()
        Config.read("config.txt")
        rabbitmq_url = Config.get('RABBITMQ', 'rabbitmq_url')
        rabbitmq_port = Config.getint('RABBITMQ', 'rabbitmq_port')
        exchangeName = Config.get('RABBITMQ', 'exchangeName')
        retrieve_routing_key = Config.get('RABBITMQ', 'retrieve_routing_key')
        refresh_rate = Config.getint('AGENTS', 'refresh_rate')

        guid = None
        try:
            guid = Config.get('AGENTS', 'guid')
        except:
            guid = str(uuid.uuid4().int >> 96)
            with open('config.txt', 'w') as f:
                Config.set('AGENTS', 'guid', guid)
                Config.write(f)

        myagent = AgentRunner(rabbitmq_url, rabbitmq_port,
                            exchangeName, retrieve_routing_key,
                            mypmem.getPhysicalMemoryAgent, 'PhysicalMemory', 
                            guid, refresh_rate)
        myagent.start()
    except KeyboardInterrupt:
        try:
            if myagent is not None:
                myagent.stop()
        except:
            pass
    except Exception, e:
        print "Exception handled...\nDetail:\n%s" % e
        try:
            if myagent is not None:
                myagent.stop()
        except:
            pass