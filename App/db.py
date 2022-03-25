import datetime
from lib2to3.pgen2.token import DOUBLESTAREQUAL
from operator import truediv
import sqlite3

#connect database
dbPath="D:\\TallerUAPA\\App\\db\\Taller.db"

def GetAllMarcas():
    #en cada funcion se debe crear un cursor para leer los datos
    dbReader=sqlite3.connect(dbPath).cursor()
    marcas=dbReader.execute("select * from Marcas").fetchall()
    dbReader.close()
    return marcas

def GetMarcasActivas():
    dbReader=sqlite3.connect(dbPath).cursor()
    marcasActivas=dbReader.execute("select marcaid,marcanombre from Marcas where activo='true'").fetchall()
    dbReader.close()
    return list(marcasActivas)

def GetModelosPorMarca(marca):
    dbReader=sqlite3.connect(dbPath).cursor()
    Modelos=dbReader.execute(f"select modeloid,modelonombre from Modelos where MarcaId={str(marca)} and activo='true'").fetchall()
    dbReader.close()
    return list(Modelos)

def GetOSCliente(orden):
    dbReader=sqlite3.connect(dbPath).cursor()
    Orden_Servicio_db=dbReader.execute(f"select * from ConsultaOSUsuario where OrdenId='{str(orden)}'").fetchone()
    dbReader.close()

    if Orden_Servicio_db:
        orden_servicio=list(Orden_Servicio_db)
        for dato in orden_servicio:
            if not dato: orden_servicio[orden_servicio.index(dato)]=0
        return orden_servicio

def GetAllOrdenesServicio():
    dbReader=sqlite3.connect(dbPath).cursor()
    Ordenes_Servicio=dbReader.execute("select * from ConsultaOS").fetchall()
    dbReader.close()

    if Ordenes_Servicio:
        return list(Ordenes_Servicio)

def GetOrdenesServicioEnTaller():
    dbReader=sqlite3.connect(dbPath).cursor()
    Ordenes_Servicio=dbReader.execute("select * from ConsultaOSEnTaller").fetchall()
    dbReader.close()

    if Ordenes_Servicio:
        return list(Ordenes_Servicio)

def CreateServiceOrder(OSrequest):   
    insert_params=""
    for param in OSrequest:
        insert_params+=  f"'{param}',"
    insert_params+=f"'{str(datetime.datetime.now())}','Para Revisar'"
    insert_query="INSERT INTO OrdenesServicio (ClienteNombre,ClienteTelefono,MarcaId,ModeloId,Año,Chasis,FallaReportada,FechaRecepcion,Estado) VALUES ("+insert_params+");"
    
    conn=sqlite3.connect(dbPath,isolation_level=None)
    dbCursor=conn.cursor()
    before=dbCursor.rowcount
    with conn:
        dbCursor.execute(insert_query)
        conn.commit()
    after=dbCursor.rowcount
    dbCursor.close()
    conn.close()

    return after>before

def UpdateDiagnose(order_id,diagnose,amount):
    if not diagnose or not amount: return False
    update_query=f"UPDATE OrdenesServicio SET Diagnostico = '{str(diagnose)}', Estado = 'Esperando Autorizacion' WHERE OrdenId = '{str(order_id)}';"
    insert_query=f"INSERT INTO Cotizaciones (FechaCotizacion,OrdenServicioId,Monto,Estado, DetalleCotizacion) VALUES ('{str(datetime.datetime.now())}','{str(order_id)}','{amount}','Esperando Autorizacion','{str(diagnose)}');"
    conn=sqlite3.connect(dbPath,isolation_level=None)
    dbCursor=conn.cursor()
    before=dbCursor.rowcount
    with conn:
        dbCursor.execute(update_query)
        dbCursor.execute(insert_query)
        conn.commit()
    after=dbCursor.rowcount
    dbCursor.close()
    conn.close()

    return after>before

def UpdateRepair(order_id,repair):
    if not repair: return False
    update_query=f"UPDATE OrdenesServicio SET Reparacion = '{str(repair)}', Estado = 'Reparado' WHERE OrdenId = '{str(order_id)}';"
    conn=sqlite3.connect(dbPath,isolation_level=None)
    dbCursor=conn.cursor()
    with conn:
        dbCursor.execute(update_query)
        conn.commit()
    dbCursor.close()
    conn.close()

    return True

def Entregar_Orden_Servicio(orden_id):
    if not orden_id: return False
    update_query=f"update ordenesservicio set estado='Entregado' where ordenid='{str(orden_id)}';"
    conn=sqlite3.connect(dbPath,isolation_level=None)
    dbCursor=conn.cursor()
    with conn:
        dbCursor.execute(update_query)
        conn.commit()
    dbCursor.close()
    conn.close()
    return True

def GetUsuario(username):
    dbReader=sqlite3.connect(dbPath).cursor()
    usuariodb=dbReader.execute(f"select * from consultausuariosactivos where usuario='{str(username)}'").fetchone()
    dbReader.close()

    return usuariodb

def Login(loginInfo):
    #ToDo: ver como hacer un hash de la contraseña
    usuariodb=GetUsuario(loginInfo[0])
    if usuariodb and usuariodb[3]==loginInfo[1]:
        return (usuariodb[0],usuariodb[1],usuariodb[4]) #UserId, User Name, User Profile
    else:
        return None