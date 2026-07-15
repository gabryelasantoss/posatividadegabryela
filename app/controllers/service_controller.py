from app.extensions import db
from app.models.service import Service, ServiceOrder
from app.schemas.service_schema import ServiceSchema, ServiceOrderSchema
from app.utils.response import success_response

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)
order_schema = ServiceOrderSchema()
orders_schema = ServiceOrderSchema(many=True)

# --- Serviços ---

def listar_servicos():
    servicos = Service.query.all()
    return success_response(services_schema.dump(servicos))

def criar_servico(data):
    dados_validados = service_schema.load(data)
    novo_servico = Service(**dados_validados)
    db.session.add(novo_servico)
    db.session.commit()
    return success_response(service_schema.dump(novo_servico), 201)

# --- Ordens de Serviço ---

def listar_ordens():
    ordens = ServiceOrder.query.all()
    return success_response(orders_schema.dump(ordens))

def criar_ordem(data):
    dados_validados = order_schema.load(data)
    
    # Validar se o serviço existe
    Service.query.get_or_404(dados_validados["service_id"])
    
    nova_ordem = ServiceOrder(**dados_validados)
    db.session.add(nova_ordem)
    db.session.commit()
    return success_response(order_schema.dump(nova_ordem), 201)

def listar_ordens_por_servico(service_id):
    # Validar se o serviço existe
    Service.query.get_or_404(service_id)
    
    ordens = ServiceOrder.query.filter_by(service_id=service_id).all()
    return success_response(orders_schema.dump(ordens))
