from marshmallow import fields

from app.extensions import ma
from app.models.message import Message


class MessageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Message

    id = ma.auto_field(dump_only=True)
    content = ma.auto_field(required=True)
    user_id = ma.auto_field(required=True)
    created_at = ma.auto_field(dump_only=True)
    user = fields.Nested("UserSchema", only=("id", "nome"))
