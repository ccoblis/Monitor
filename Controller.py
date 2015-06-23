from db import api as db_api
import ConfigParser
import time
from SimpleMessagePassing import SimpleMessagePassing
import json


def onDataRetrieve(channel, method, properties, body):
    try:
        id = int(properties.correlation_id)
        print 'Adding data to database'
        print '* ID: %d' % (id)
        print '* Info: %s' % (body)
        info = db_api.get_data_id(id)
        if info is not None:  #we need to update data from db
            print 'Updating GUID %d' % (id)
            agent = json.loads(body)
            info_agent = json.loads(info.data)
            agent_name = agent.keys()[0]
            if agent_name in info_agent:  #update info
                info_agent.update(agent)
            else:
                info_agent[agent_name] = agent  #add new agent
            body = json.dumps(info_agent)

        db_api.add_data(id, body)  #we add it
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception, e:
        channel.basic_nack(delivery_tag=method.delivery_tag)
        print e

if __name__ == "__main__":
    messagepassing = None
    while True:
        try:
            print 'Initializing controller...'
            Config = ConfigParser.ConfigParser()
            Config.read("config.txt")
            rabbitmq_url = Config.get('RABBITMQ', 'rabbitmq_url')
            rabbitmq_port = Config.getint('RABBITMQ', 'rabbitmq_port')
            exchangeName = Config.get('RABBITMQ', 'exchangeName')
            retrieve_routing_key = Config.get('RABBITMQ', 'retrieve_routing_key')
        
            messagepassing = SimpleMessagePassing(rabbitmq_url,
                                                  rabbitmq_port)

            print 'Start consuming...'
            messagepassing.run(
                    callback_onMessage=onDataRetrieve,
                    exchangeName=exchangeName,
                    requestQueue=None,
                    consume_routing_key=retrieve_routing_key,
                    publish_rounting_key=None,
                    message_body=None)
        except KeyboardInterrupt:
            try:
                if messagepassing is not None:
                    messagepassing.stop()
            except:
                pass
            finally:
                break
        except Exception, e:
            # Reconnect on exception
            print "Exception handled, reconnecting...\nDetail:\n%s" % e
            try:
                if messagepassing is not None:
                    messagepassing.stop()
            except:
                pass
            time.sleep(5)
