from app.extensions import db


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco_base = db.Column(db.Float, nullable=False)

    orders = db.relationship("ServiceOrder", backref="service", lazy=True)


class ServiceOrder(db.Model):
    __tablename__ = "service_orders"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="aberta")
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
