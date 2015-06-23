import time
from SimpleMessagePassing import SimpleMessagePassing
import uuid
import json


class AgentRunner(object):
    def __init__(self, rabbitmq_url, rabbitmq_port,
                    exchangeName,
                    retrieve_routing_key,
                    func, name='Unknown', guid = None,
                    refresh_rate = 30):
        self.messagepassing = None
        if guid is None:
            self.guid = str(uuid.uuid4().int >> 96)
        else:
            self.guid = guid
        self.agentName = name
        self.retrieve_func = func
        self.rabbitmq_url = rabbitmq_url
        self.rabbitmq_port = rabbitmq_port
        self.exchangeName = exchangeName
        self.retrieve_routing_key = retrieve_routing_key
        self.refresh_rate = refresh_rate

    def start(self):        
        print 'Agent GUID: %s' % (self.guid)
        print 'Initializing %s agent ...' % (self.agentName)
        messagepassing = SimpleMessagePassing(self.rabbitmq_url,
                                              self.rabbitmq_port)
        print 'Start sending...'
        while True:
            print 'Retrieving %s agent status...' % (self.agentName),
            data_from_agent = {}
            data_from_agent[self.agentName] = self.retrieve_func()
            request_body = json.dumps(data_from_agent)
            print 'done'
            print 'Sending request...',
            result = messagepassing.run(
                        callback_onMessage=None,
                        exchangeName=self.exchangeName,
                        requestQueue=None,
                        consume_routing_key=None,
                        publish_rounting_key=self.retrieve_routing_key,
                        message_body=str(request_body),
                        id=self.guid)

            if result is True:
                print 'done'
            else:
                print 'error'

            print 'Retrieving new %s agent status in %d seconds' \
                % (self.agentName, self.refresh_rate)
            time.sleep(self.refresh_rate)

    def stop(self):
        if messagepassing is not None:
            messagepassing.stop()