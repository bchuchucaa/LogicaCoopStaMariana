from typing import Optional
from pydantic import BaseModel


class Usuario_API(BaseModel):
    id: str
    nombre : str
    apellido: str
    direccion: str
    correo: str
    rol: Optional[str] = None
    password: str

    def __repr__(self) -> str:
        return f'ID: {self.id}, Nombre: {self.nombre}, Apellido: {self.apellido}, ' \
               f'Direccion: {self.direccion}, Rol: {self.rol}, ' \
               f'Password: {self.password}'


class Usuario_Login_API(BaseModel):
    correo: str
    password: str


class Usuario_Get(BaseModel):
    id: str
    nombre: str
    apellido: str
    direccion: str
    correo: str


class Derecho_Create_API(BaseModel):
    fecha_adquisicion: str
    numero_medidor: str
    usuario_id: str


class Derecho_Get(BaseModel):
    id: int
    fecha: str
    numero_medidor: str
    usuario_id: str

class Lectura_Create_API(BaseModel):
    fecha:str
    lecturaAnterior:float
    lecturaActual:float
    consumo:float
    exceso:float
    derechoAgua:int
