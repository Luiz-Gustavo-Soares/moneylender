from app import db
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash

class Devedores(db.Model):
    __tablename__ = 'devedores'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    foto_perfil = db.Column(db.String(250))

    def __repr__(self):
        return '<Devedor %r>' % self.nome


class Dividas(db.Model):
    __tablename__ = 'dividas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meses_devendo = db.Column(db.Integer())
    devedor_id = db.Column(db.Integer, db.ForeignKey('devedores.id'))
    devedor = db.relationship("Devedores", backref=backref("devedores", uselist=False))

    def __repr__(self):
        return '<Divida %r>' % self.id


class Config(db.Model):
    __tablename__ = 'config'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dia_cobranca = db.Column(db.String(100))
    valor = db.Column(db.Float())

    def __repr__(self):
        return '<Config %r>' % self.id
    

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(150))
    senha = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150))

    def __init__(self, usuario, senha, email='', id=1):
        self.id = id
        self.usuario = usuario
        self.senha = generate_password_hash(senha)
        self.email = email

    def verify_senha(self, senha):
        return check_password_hash(self.senha, senha)


    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<Login %r>' % self.usuario
