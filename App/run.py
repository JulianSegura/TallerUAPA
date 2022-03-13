from flask import Flask, render_template, request
import db


#create controllers App
app=Flask(__name__)

#Index
@app.route("/", methods=['GET','POST'])
def Index():
    OSQueryResult="firsttime"
    if request.method=='POST' and 'txtOrdenServicio' in request.form:
        NumeroOrden=request.form['txtOrdenServicio']
        if NumeroOrden != "":
            OSQueryResult=db.ConsultaOSCliente(NumeroOrden)

    return render_template("tallerindex.html",DatosConsulta=OSQueryResult)

@app.route("/login")
def Login():
    Marcas=db.GetAllMarcas()
    detalleMarcas=""
    if Marcas:
        detalleMarcas="<table>"
        for marca in Marcas:
            detalleMarcas=detalleMarcas+"<tr><td>"+marca[1]+"</td></tr>"
        detalleMarcas=detalleMarcas+"</table>"

    return "Login para ingresar al sistema "+detalleMarcas


@app.route("/contacto")
def Contacto():
    return "Aqui va la pagina para contactarnos"


#Application Entry Point
if __name__ == "__main__":
    app.run(debug=True)

