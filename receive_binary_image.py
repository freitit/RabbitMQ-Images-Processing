try:
    import pika
    import ast
    import time
    from PIL import Image as image
    from datetime import datetime

except Exception as e:
    print("Some modules are missings {}".format(e))


class MetaClass(type):

    _instance ={}

    def __call__(cls, *args, **kwargs):

        """ Singelton Design Pattern  """

        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class RabbitMqServerConfigure(metaclass=MetaClass):

    def __init__(self, host='localhost'):

        """ Server initialization   """

        self.host = host


class rabbitmqServer():

    def __init__(self, server):

        """
        :param server: Object of class RabbitMqServerConfigure
        """

        self.server = server
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        print("Server started waiting for Messages ")

    @staticmethod
    def callback_app1(ch,method, properties, body):

        Payload = body.decode("utf-8")
        Payload = ast.literal_eval(Payload)
        
        # datetime object containing current date and time
        now = datetime.now()

        # dd/mm/YY H:M:S
        path = "I:/daihoc/nam4/ky_II/ThayHa_LapTrinhWebVaUngDung/thuchanh/xampp/htdocs/imagegallery/images/app1/"
        dt_string = now.strftime("app1_%d%m%Y%H%M%S.png")
        file_name = path + dt_string

        with open(file_name, "wb") as f:
            f.write(Payload)

        

        print(type(Payload))
        print("Data Received")

    @staticmethod
    def callback_app2(ch,method, properties, body):

        Payload = body.decode("utf-8")
        Payload = ast.literal_eval(Payload)
        image
        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        path = "I:/daihoc/nam4/ky_II/ThayHa_LapTrinhWebVaUngDung/thuchanh/xampp/htdocs/imagegallery/images/app2/"
        dt_string = now.strftime("app2_%d%m%Y%H%M%S.png")
        file_name = path + dt_string

        with open(file_name, "wb") as f:
            f.write(Payload)

        color_img = image.open(file_name)
        bi_img = color_img.convert("1")
        bi_img.save(file_name)

        print(type(Payload))
        print("Data Received")

    def startserver(self, callback):
        self._channel.exchange_declare(exchange='topic', exchange_type='fanout')
        result = self._channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        self._channel.queue_bind(exchange='topic', queue=queue_name)
        print(' [*] Waiting for signals. To exit press CTRL+C')
        self._channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True)
        self._channel.start_consuming()


if __name__ == "__main__":
    serverconfigure = RabbitMqServerConfigure(host='localhost')

    server = rabbitmqServer(server=serverconfigure)
    server.startserver(rabbitmqServer.callback_app2)