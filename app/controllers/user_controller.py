from app.extensions import db
from app.models.user import User
from app.schemas.user_schema import UserSchema
from app.utils.response import success_response
from werkzeug.exceptions import Unauthorized
from flask_jwt_extended import create_access_token


user_schema = UserSchema()
users_schema = UserSchema(many=True)


def listar_usuarios():
    usuarios = User.query.all()
    return success_response(users_schema.dump(usuarios))


def criar_usuario(data):
    dados_validados = user_schema.load(data)
    senha = dados_validados.pop('senha')
    novo_usuario = User(**dados_validados)
    novo_usuario.set_senha(senha)

    db.session.add(novo_usuario)
    db.session.commit()

    return success_response(user_schema.dump(novo_usuario), 201)


def atualizar_usuario(id, data):
    usuario = User.query.get_or_404(id)

    dados_validados = user_schema.load(data, partial=True)
    if 'senha' in dados_validados:
        senha = dados_validados.pop('senha')
        usuario.set_senha(senha)

    for campo, valor in dados_validados.items():
        setattr(usuario, campo, valor)

    db.session.commit()

    return success_response(user_schema.dump(usuario))


def deletar_usuario(id):
    usuario = User.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return "", 204


def login(data):
    email = data.get('email')
    senha = data.get('senha')
    
    if not email or not senha:
        raise Unauthorized('Email e senha são necessários')
    
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_senha(senha):
        raise Unauthorized('Credenciais inválidas')
    
    access_token = create_access_token(identity=str(user.id))
    return success_response({'access_token': access_token})
