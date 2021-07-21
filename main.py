from pydantic.errors import FloatError
import uvicorn
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from datetime import datetime

from model.model import Base, Usuario, Trabajo, DerechoAgua,Lectura,Pago
from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker


def create_session():
    engine = create_engine('postgresql://consultas:QueryConSql.pwd@localhost/coop_st_mariana')
    Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


from fastapi import FastAPI, File, UploadFile, HTTPException
from starlette.middleware.cors import CORSMiddleware
from model.api_model import Lectura_Create_API, Usuario_API, Usuario_Login_API, Usuario_Get, Derecho_Create_API, Derecho_Get,Pago_Api_Exec

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)


@app.post('/register/', status_code=200)
async def register(usuario: Usuario_API):
    try:
        print(usuario.__repr__())
        session = create_session()
        usuario = Usuario(id=usuario.id, nombre=usuario.nombre, apellido=usuario.apellido, direccion=usuario.direccion,
                          correo=usuario.correo,
                          password=usuario.password, rol='cliente')
        session.add(usuario)
        session.commit()
        session.close()

        return {'ESTADO': 'Correcto!'}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400)


@app.post('/login/')
async def login(usuario: Usuario_Login_API):
    print(usuario.__repr__())
    session = create_session()
    try:
        result: Usuario = session.query(Usuario).filter(Usuario.correo == usuario.correo,
                                                        Usuario.password == usuario.password).one()
        session.close()
        return {'ESTADO': 'CORRECTO', 'id': result.id, 'nombre': result.nombre, 'apellido': result.apellido,
                'direccion': result.direccion,
                'correo': result.correo, 'rol': result.rol}
    except MultipleResultsFound as mrf:
        raise HTTPException(status_code=404, detail="Hay mas de un registro con los datos")
    except NoResultFound as nrf:
        print('ERROR: No hay resultados!')
        raise HTTPException(status_code=404, detail='No hay ningun usuario')


@app.post('/user/update')
async def user_update(usuario: Usuario_Login_API):

    ...


@app.post('/derecho/create')
async def derecho_create(derecho: Derecho_Create_API):
    session = create_session()
    try:
        print(derecho.fecha_adquisicion)
        derecho_agua = DerechoAgua(fechaAdquisicion=datetime.strptime(derecho.fecha_adquisicion, '%d/%m/%Y'), numeroMedidor=derecho.numero_medidor,
                                   usuario_id=derecho.usuario_id)
        session.add(derecho_agua)
        session.commit()
        session.close()
        return {'Hola': 'Al parecer si se guardo bien ajio ajio'}
    except Exception as e:
        print(e)
        print('ERRORRRRRRRRRRRRRR')
    ...

@app.post('/lectura/create')
async def lectura_create(lectura:Lectura_Create_API):
    session = create_session()
    try:
        result = session.query(Lectura).filter(Lectura.derechoAgua == lectura.derechoAgua)
        maxid= max((lecture.id for lecture in result),default=0)
        if(maxid!=0):
            last_lecture= Lectura()
            for lecture in result:
                if(lecture.id==maxid):
                    last_lecture=lecture
            lectura= Lectura(fecha= datetime.strptime(lectura.fecha,'%d/%m/%Y'),lecturaActual=lectura.lecturaActual,consumo=lectura.lecturaActual-last_lecture.lecturaActual,exceso=lectura.exceso,estado="pendiente",derechoAgua=lectura.derechoAgua)
        else:
            lectura= Lectura(fecha= datetime.strptime(lectura.fecha,'%d/%m/%Y'),lecturaActual=lectura.lecturaActual,consumo=lectura.lecturaActual,exceso=lectura.exceso,estado="pendiente",derechoAgua=lectura.derechoAgua)
        session.add(lectura)
        session.commit()
        session.close()
        return {'RESPUESTA':'OK'}
    except Exception as e:
        print(e)
        print('ALGO SALIO MAL REVISA EL METODO LECTURA CREATE')
    ...
@app.post('/pago/ejecutar')
async def pago_create(pago:Pago_Api_Exec):
    session = create_session()
    try:
        pago= Pago(atraso=pago.atraso,otros=pago.otros,mensual=pago.mensual, mora=pago.mora,total=pago.total,lectura=pago.lectura)
        session.add(pago)
        session.query(Lectura).filter(Lectura.id == pago.lectura).update({'estado': 'liquidado'})
        session.commit()
        session.close()
        return {'RESPUESTA':'OK'}
    except Exception as e:
        print(e)
        print('Review payment create method')
    ...
#Get user lecturas for payment
@app.get('/lectura/usuario/', response_model=list[Lectura_Create_API])
async def lectura_get(cedula: str):
    session = create_session()
    try:
        derecho = session.query(DerechoAgua).filter(DerechoAgua.usuario_id == cedula).one_or_none()
        result = session.query(Lectura).filter(Lectura.derechoAgua == derecho.id)
        lecturas = []
        for rst in result:
            if(rst.estado=="pendiente"):
                lectura = {'id': rst.id, 'fecha': str(rst.fecha), 'estado': rst.estado,
                       'lecturaActual': rst.lecturaActual,'consumo':rst.consumo,'exceso':rst.exceso,'derechoAgua':rst.derechoAgua}
                lecturas.append(lectura)
        session.close()
        return lecturas
    except Exception as e:
        print(e)


@app.get('/user/users', response_model=list[Usuario_Get])
async def user_get():
    session = create_session()
    try:
        result = session.query(Usuario).all()
        usuarios = []
        for rst in result:
            usuario = {'id': rst.id, 'nombre': rst.nombre, 'apellido': rst.apellido,
                             'direccion': rst.direccion, 'correo': rst.correo}
            usuarios.append(usuario)
        return usuarios
    except Exception as e:
        print(e)


@app.get('/derecho/derechos', response_model=list[Derecho_Get])
async def derecho_get():
    session = create_session()
    try:
        result = session.query(DerechoAgua).all()
        usuarios = []
        for rst in result:
            usuario = {'id': rst.id, 'fecha': str(rst.fechaAdquisicion), 'numero_medidor': rst.numeroDeMedidor, 'usuario_id': rst.usuario_id}
            usuarios.append(usuario)
        return usuarios
    except Exception as e:
        print(e)

@app.get('/derecho/derechos/', response_model=list[Derecho_Get])
async def derecho_get(cedula: str):
    session = create_session()
    try:
        result = session.query(DerechoAgua).filter(DerechoAgua.usuario_id == cedula)
        usuarios = []
        for rst in result:
            usuario = {'fecha': str(rst.fechaAdquisicion), 'numero_medidor': rst.numeroDeMedidor,
                       'usuario_id': rst.usuario_id}
            usuarios.append(usuario)
        session.close()
        return usuarios
    except Exception as e:
        print(e)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', reload=True)
