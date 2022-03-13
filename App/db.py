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
    Modelos=dbReader.execute("select * from Modelos where MarcaId=" + str(marca)).fetchall()
    dbReader.close()
    return Modelos

def ConsultaOSCliente(orden):
    dbReader=sqlite3.connect(dbPath).cursor()
    Orden_Servicio=dbReader.execute("select * from ConsultaOSUsuario where OrdenId=" + str(orden)).fetchall()
    dbReader.close()

    if len(Orden_Servicio)> 0:
        return Orden_Servicio[0]
    # else:
    #     return None

    