import pika


class SimpleMessagePassing(object):
    def __init__(self, host='localhost', port=5672):
        self._connection = None
        self._host = host
        self._port = port
        self._channel = None
        self._isConnected = False

    def connect(self):
        if not self._isConnected:
            self._isConnected = True
            return pika.BlockingConnection(
                    pika.ConnectionParameters(host=self._host,
                                              port=self._port))
        return self._connection

    def stop(self):
        if self._isConnected:
            self._channel.stop_consuming()
            self._connection.close()
            self._isConnected = False

    def open_channel(self):
        return self._connection.channel()

    def run(self, callback_onMessage, exchangeName='',
                requestQueue=None,
                consume_routing_key='query',
                publish_rounting_key='retrieve',
                message_body='Test',
                id=None,
                no_consumer_ack=False):

        if not self._isConnected:
            self._connection = self.connect()
            self._channel = self.open_channel()

        if requestQueue is None:
            result = self._channel.queue_declare(exclusive=True)
            requestQueue = result.method.queue
        else:
            self._channel.queue_declare(queue=requestQueue)

        if not no_consumer_ack:
            # Turn on delivery confirmations
            self._channel.confirm_delivery()

        if exchangeName != '':
            self._channel.exchange_declare(
                        exchange=exchangeName,
                        exchange_type="direct")
            if consume_routing_key is not None:
                self._channel.queue_bind(
                        exchange=exchangeName,
                        queue=requestQueue,
                        routing_key=consume_routing_key)

        if callback_onMessage is not None:
            self._channel.basic_consume(
                        consumer_callback=callback_onMessage,
                        queue=requestQueue,
                        no_ack=no_consumer_ack)

        status = False
        if publish_rounting_key is not None:
            if id is not None:
                status = self._channel.basic_publish(
                        exchange=exchangeName,
                        routing_key=publish_rounting_key,
                        body=message_body,
                        properties=pika.BasicProperties(
                            delivery_mode=2,
                            correlation_id=id,))
            else:
                status = self._channel.basic_publish(
                        exchange=exchangeName,
                        routing_key=publish_rounting_key,
                        body=message_body)

        if callback_onMessage is not None:
            self._channel.start_consuming()
        else:
            return status

    def __del__(self):
        self.stop()
