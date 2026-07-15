from marshmallow import fields
from app.extensions import ma
from app.models.service import Service, ServiceOrder


class ServiceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Service

    id = ma.auto_field(dump_only=True)
    nome = ma.auto_field(required=True)
    descricao = ma.auto_field()
    preco_base = ma.auto_field(required=True)


class ServiceOrderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ServiceOrder

    id = ma.auto_field(dump_only=True)
    descricao = ma.auto_field(required=True)
    status = ma.auto_field()
    service_id = ma.auto_field(required=True)
