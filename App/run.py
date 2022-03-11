from itertools import count
from flask import Flask, render_template, request
import db


#create controllers App
#app=Flask(__name__)

marcas=db.GetAllMarcas()
print ("Total de marcas: ",len(marcas))

marcasActivas=db.GetMarcasActivas()
if len(marcasActivas)>0:
    for marca in marcasActivas:
        print(marca[1])
else:
    print("No se han agregado marcas")





#Application Entry Point
#if __name__ == "__main__":
    #app.run(debug=True)

