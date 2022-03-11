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
    Modelos=dbReader.execute("select * from Modelos where MarcaId=" + marca).fetchall()
    dbReader.close()
    return Modelos
