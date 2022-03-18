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
    marcasActivas=dbReader.execute("select * from Marcas where activo=1").fetchall()
    dbReader.close()
    return marcasActivas

def GetModelosPorMarca(marca):
    dbReader=sqlite3.connect(dbPath).cursor()
    Modelos=dbReader.execute(f"select * from Modelos where MarcaId='{str(marca)}'").fetchall()
    dbReader.close()
    return Modelos

def ConsultaOSCliente(orden):
    dbReader=sqlite3.connect(dbPath).cursor()
    Orden_Servicio=dbReader.execute(f"select * from ConsultaOSUsuario where OrdenId='{str(orden)}'").fetchone()
    dbReader.close()

    if Orden_Servicio:
        return Orden_Servicio

def GetUsuario(username):
    
    dbReader=sqlite3.connect(dbPath).cursor()
    usuariodb=dbReader.execute(f"select * from consultausuariosactivos where usuario='{str(username)}'").fetchone()
    dbReader.close()

    return usuariodb

def Login(loginInfo):
    #ToDo: ver como hacer un hash de la contraseña
    usuariodb=GetUsuario(loginInfo[0])
    if usuariodb != None and usuariodb[3]==loginInfo[1]:
        return (usuariodb[0],usuariodb[1],usuariodb[4])
    else:
        return None