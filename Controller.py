from db import api as db_api
import config
import time
from SimpleMessagePassing import SimpleMessagePassing


def onDataRetrieve(channel, method, properties, body):
    print 'Adding data to database'
    try:
        # print body
        id = int(properties.correlation_id)
        db_api.add_data(id, body)

        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception, e:
        channel.basic_nack(delivery_tag=method.delivery_tag)
        print e

if __name__ == "__main__":
    messagepassing = None
    while True:
        try:
            print 'Initializing controller...'
            messagepassing = SimpleMessagePassing(config.rabbitmq_url,
                                                  config.rabbitmq_port)

            print 'Start consuming...'
            messagepassing.run(
                    callback_onMessage=onDataRetrieve,
                    exchangeName=config.exchangeName,
                    requestQueue=None,
                    consume_routing_key=config.retrieve_routing_key,
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
