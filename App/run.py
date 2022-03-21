from datetime import timedelta
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
import db


#create controllers App
app=Flask(__name__)
app.secret_key="NuestraLlaveSecreta"
app.permanent_session_lifetime=timedelta(minutes=10)

#Index
@app.route("/", methods=['GET','POST'])
def Index():
    if request.method=='POST' and 'txtOrdenServicio' in request.form:
        NumeroOrden=request.form['txtOrdenServicio']
        if NumeroOrden == "": return render_template("tallerindex.html",DatosConsulta="emptyQuery")
        OSQueryResult=db.GetOSCliente(NumeroOrden)
        return render_template("tallerindex.html",DatosConsulta=OSQueryResult)
        
    else:
        #Jinja is not letting me clear the cache so i need to send the variable as empty
        return render_template("tallerindex.html",DatosConsulta="emptyQuery")


#Login Page
@app.route("/login", methods=['GET','POST'])
def Login():
    session.clear()
    if request.method=='POST' and 'txtUsuario' and 'txtPassword' in request.form:
        validInfo=request.form['txtUsuario'] != "" and request.form['txtPassword'] != ""
        #If user or password is empty with return invalid credentials
        if not validInfo: return render_template("login.html",Results="Credenciales Invalidos")

        LoginResults=db.Login((request.form['txtUsuario'],request.form['txtPassword']))
        
        #if user cannot login will return nothing
        if not LoginResults: return render_template("login.html",Results=None)

        #load session dictionary and render appropiate template
        session['userId']=LoginResults[0]
        session['UserName']=LoginResults[1]
        session['UserProfile']=LoginResults[2]
        session.permanent=True

        match session['UserProfile']:
            case "Admin":
                return redirect(url_for('Admin'))
            case "Mecanico":
                return redirect(url_for('Taller'))

    #When method is not post, it will GET the page
    else:
        return render_template("login.html")

#Admin Page
@app.route("/admin", methods=['GET','POST'])
def Admin():
    if not session or session['UserProfile'] != "Admin":
        return redirect(url_for('Login'))        
    if request.method == 'GET': 
        ordenesServicio=GetOrdenesServicio()
        Marcas=db.GetMarcasActivas()
        return render_template("admin.html",OrdenesServicio=ordenesServicio,marcas=Marcas)
    else:
        return RegisterOS()

def GetOrdenesServicio():
    ordenes=db.GetAllOrdenesServicio()
    if not ordenes: return None
    ordenesToReturn=[]
    for orden in ordenes:
        orden=list(orden)
        #convert diasEnTaller to int
        orden[2]=int(orden[2])
        #if Reparacion have data, we return the reparacion data, else we return the Diagnostico data
        if orden[9] == None:
            orden.remove(orden[9])
        else:
            orden.remove(orden[8])
        ordenesToReturn.append(orden)
    return ordenesToReturn

#Register Service Order
def RegisterOS():
    OSRequest=(request.form['txtNombreCliente'],request.form['txtTelefonoCliente'],request.form.get('cmbMarca'),request.form.get('cmbModelo'),
    request.form['txtAno'],request.form['txtChasis'],request.form['txtReportedFailure'])
    creation_result = db.CreateServiceOrder(OSRequest)
    if creation_result:
        flash("Orden De Servicio Creada Correctamente")
        return redirect(url_for('Admin'))
    else:
        return "NO SE GUARDO"

@app.route("/models/<marcaid>")
def ModelsByBrand(marcaid):
    models=db.GetModelosPorMarca(marcaid)
    modelsToReturn=[]
    for model in models:
        modelobj={}
        modelobj['modelId']=model[0]
        modelobj['modelName']=model[1]
        modelsToReturn.append(modelobj)
    return jsonify({'models':modelsToReturn})

#Taller Page
@app.route("/taller")
def Taller():
    if not session or session['UserProfile']!="Mecanico":
        return redirect(url_for('Login'))
    return "Pagina de personal de taller"

#Contact Page
@app.route("/contacto")
def Contacto():
    return "Aqui va la pagina para contactarnos"

#Application Entry Point
if __name__ == "__main__":
    app.run(debug=True)

