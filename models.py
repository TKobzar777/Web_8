
from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE, EmailField, BooleanField

uri = "mongodb+srv://user1:******@tetianakobzar.2kizr3f.mongodb.net/?retryWrites=true&w=majority&appName=TetianaKobzar"

connect(db="TetianaKobzar", host=uri)


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)


class Contact(Document):
    full_name = StringField(required=True, max_length=100)
    email = EmailField(required=True, unique=True)
    phone_number = StringField(max_length=20)
    message_sent = BooleanField(default=False)
    preferred_contact_method = StringField(choices=["email", "sms"], default="email")
