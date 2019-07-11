from mongoengine import StringField, \
    BinaryField, Document, IntField,\
    BooleanField, DateTimeField
from datetime import datetime


class ImageHandler(Document):
    md5 = StringField(required=True, max_length=200)
    original_image = BinaryField()
    grey_image = BinaryField()
    width = IntField(required=True, max_length=50)
    height = IntField(required=True, max_length=50)
    created_at = DateTimeField(default=datetime.utcnow())
    meta = {
        'indexes': [
            {'fields': ['md5'], 'unique': True}
        ]
    }


class ImageStatus(Document):
    url = StringField(required=True, max_length=200)
    with_error = BooleanField(required=True, default=False)
    created_at = DateTimeField(default=datetime.utcnow())
    meta = {
        'indexes': [
            {'fields': ['url'], 'unique': True}
        ]
    }
