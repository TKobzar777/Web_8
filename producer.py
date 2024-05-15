import pika
import random

from faker import Faker
from mongoengine.errors import NotUniqueError

from models import Contact


def main():
    fake = Faker('uk-UA')
    # Подключение к RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Создание очередей с именами 'email_queue' и 'sms_queue'
    channel.queue_declare(queue="email_queue")
    channel.queue_declare(queue="sms_queue")

    # Генерация контактов и отправка их в соответствующие очереди

    contacts_data = []
    try:
        for _ in range(6):
            contact_per = Contact(full_name=fake.full_name(), email=fake.email(), phone_number=fake.phone_number(),
                                  message_sent=fake.random_choices([True, False]),
                                  preferred_contact_method=random.choice(["email", "sms"]))

            contact_per.save()
            message = str(contact_per.id)

            # Отправка сообщения в соответствующую очередь в зависимости от предпочтительного метода связи
            if contact_per.preferred_contact_method == "email":
                channel.basic_publish(exchange="", routing_key="email_queue", body=message.encode('utf-8'))
            elif contact_per.preferred_contact_method == "sms":
                channel.basic_publish(exchange="", routing_key="sms_queue", body=message.encode('utf-8'))

            print(f" [x] Sent '{message}' to {contact_per.preferred_contact_method}")

    except NotUniqueError:
        print(f"ото така фігня!")
    connection.close()


if __name__ == '__main__':
    main()
