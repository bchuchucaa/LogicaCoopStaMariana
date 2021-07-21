import sqlalchemy.sql
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Table, Date, Float
from sqlalchemy import Sequence
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


UsuarioTrabajo = Table('UsuarioTrabajo',
                       Base.metadata,
                       Column('id', Integer, primary_key=True),
                       Column('usuarioId', String(10), ForeignKey('Usuario.id')),
                       Column('trabajoId', Integer, ForeignKey('Trabajo.id')))


class Usuario(Base):
    __tablename__ = 'Usuario'

    id = Column(String(10), primary_key=True)
    nombre = Column(String(250))
    apellido = Column(String(250))
    direccion = Column(String(250))
    # Nuevos campos
    correo = Column(String(250))
    rol = Column(String(250))
    password = Column(String(250))

    def __init__(self, id, nombre, apellido, direccion, correo, password, rol='CLIENTE'):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.correo = correo
        self.rol = rol
        self.password = password


class Trabajo(Base):
    __tablename__ = 'Trabajo'

    id = Column(Integer, Sequence('trabajo_id_seq'), primary_key=True)
    fecha = Column(String(250))
    descripcion = Column(String(250))
    usuarios = relationship('Usuario', secondary=UsuarioTrabajo, backref='Trabajo')

    def __init__(self, fecha, descripcion):
        self.fecha = fecha
        self.descripcion = descripcion


class DerechoAgua(Base):
    __tablename__ = 'DerechoAgua'

    id = Column(Integer, Sequence('derecho_agua_id_seq'), primary_key=True)
    fechaAdquisicion = Column(Date)
    numeroDeMedidor = Column(String(250))
    usuario_id = Column(String(10), ForeignKey('Usuario.id'))

    def __init__(self, fechaAdquisicion, numeroMedidor, usuario_id):
        self.id = None
        self.fechaAdquisicion = fechaAdquisicion
        self.numeroDeMedidor = numeroMedidor
        self.usuario_id = usuario_id


class Lectura(Base):
    __tablename__ = "Lectura"

    id = Column(Integer, Sequence('lectura_id_seq'), primary_key=True)
    fecha = Column(Date)
    lecturaActual = Column(Float)
    consumo = Column(Float)
    exceso = Column(Float)
    subtotal = Column(Float)
    estado = Column(String(10))
    derechoAgua = Column(Integer, ForeignKey(DerechoAgua.id))


class Pago(Base):
    __tablename__ = 'Pago'

    id = Column(Integer, Sequence('pago_id_seq'), primary_key=True)
    atraso = Column(Float)
    otros = Column(Float)
    mensual = Column(Float)
    mora = Column(Float)
    total = Column(Float)
    lectura = Column(Integer, ForeignKey(Lectura.id))
