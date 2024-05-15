import pika
from models import Contact

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Создание очереди с именем 'email_queue'
channel.queue_declare(queue="email_queue")


def send_email(contact_id):
    print(f"Sending email to contact with ID: {contact_id}")
    contact = Contact.objects.get(id=contact_id)
    contact.message_sent = True
    contact.save()


def callback(ch, method, properties, body):
    contact_id = body.decode("utf-8")

    # Имитация отправки электронного сообщения
    send_email(contact_id)

    print(f" [x] Received '{body}'")


channel.basic_consume(queue="email_queue", on_message_callback=callback, auto_ack=True)

print(" [*] Waiting for email messages. To exit press Ctrl+C")
channel.start_consuming()