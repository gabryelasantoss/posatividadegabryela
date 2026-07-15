from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.controllers.service_controller import (
    listar_servicos,
    criar_servico,
    listar_ordens_por_servico
)

services_bp = Blueprint("services", __name__)

@services_bp.route("", methods=["GET"])
def get_services():
    response, status = listar_servicos()
    return jsonify(response), status

@services_bp.route("", methods=["POST"])
@jwt_required()
def post_service():
    data = request.get_json()
    response, status = criar_servico(data)
    return jsonify(response), status

@services_bp.route("/<int:service_id>/orders", methods=["GET"])
def get_service_orders(service_id):
    response, status = listar_ordens_por_servico(service_id)
    return jsonify(response), status
