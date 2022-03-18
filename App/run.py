from flask import Flask, redirect, render_template, request, url_for
import db


#create controllers App
app=Flask(__name__)

#Index
@app.route("/", methods=['GET','POST'])
def Index():
    OSQueryResult="emptyQuery"
    if request.method=='POST' and 'txtOrdenServicio' in request.form:
        NumeroOrden=request.form['txtOrdenServicio']
        if NumeroOrden != "":
            OSQueryResult=db.ConsultaOSCliente(NumeroOrden)

    return render_template("tallerindex.html",DatosConsulta=OSQueryResult)

@app.route("/login", methods=['GET','POST'])
def Login():
    LoginResults=""
    if request.method=='POST' and 'txtUsuario' and 'txtPassword' in request.form:
        validInfo=request.form['txtUsuario']!="" and request.form['txtPassword']!=""
        if not validInfo: 
            LoginResults="Credenciales Invalidos"
        else:
            loginInfo=request.form['txtUsuario'],request.form['txtPassword']
            LoginResults=db.Login(loginInfo)
    
    if LoginResults and LoginResults[2]=="Admin": return redirect(url_for('Admin'))
    elif LoginResults and LoginResults[2]=="Mecanico": return redirect(url_for('Taller'))
    else: return render_template("login.html",LoggedUser=LoginResults)

@app.route("/taller")
def Taller():
    return "Pagina de personal de taller"

@app.route("/admin")
def Admin():
    return render_template("admin.html")


@app.route("/contacto")
def Contacto():
    return "Aqui va la pagina para contactarnos"


#Application Entry Point
if __name__ == "__main__":
    app.run(debug=True)

