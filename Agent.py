import time
from agents.api import Agents
import config
from SimpleMessagePassing import SimpleMessagePassing
import uuid


if __name__ == "__main__":
    messagepassing = None
    guid = str(uuid.uuid4().int >> 96)
    print 'Agent GUID: %s' % (guid)
    while True:
        try:
            print 'Initializing agent...'
            messagepassing = SimpleMessagePassing(config.rabbitmq_url,
                                                  config.rabbitmq_port)
            print 'Start sending...'
            myAgent = Agents()

            while True:
                print 'Retrieving agents status...',
                request_body = myAgent.getSerializedAgents()
                print 'done'
                print 'Sending request...',
                result = messagepassing.run(
                            callback_onMessage=None,
                            exchangeName=config.exchangeName,
                            requestQueue=None,
                            consume_routing_key=None,
                            publish_rounting_key=config.retrieve_routing_key,
                            message_body=str(request_body),
                            id=guid)

                if result is True:
                    print 'done'
                else:
                    print 'error'

                print 'Retrieving new agents status in %d seconds' \
                    % (config.refresh_rate)
                time.sleep(config.refresh_rate)
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
