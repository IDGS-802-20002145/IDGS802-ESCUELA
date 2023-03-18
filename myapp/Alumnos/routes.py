from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask import jsonify
from config import DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
from models import db
from models import Alumnos
import forms

alumnos= Blueprint('alumnos', __name__)


@alumnos.route("/insertar",methods=['GET', 'POST'])
def index():
    create_form=forms.UserForm(request.form)
    if request.method == 'POST':
        alum = Alumnos(nombre=create_form.nombre.data,
                       apellidos=create_form.apellidos.data,
                       email=create_form.email.data)
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('alumnos.ABCompleto'))
    
    return render_template('index.html',form=create_form)

    

@alumnos.route("/modificar",methods=['GET','POST'])
def modificar():
    create_fprm=forms.UserForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        print('Esto es el id: ',id)
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_fprm.id.data=request.args.get('id')
        create_fprm.nombre.data=alum1.nombre
        create_fprm.apellidos.data=alum1.apellidos
        create_fprm.email.data=alum1.email
    if request.method=='POST':
        id=create_fprm.id.data
        alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.nombre=create_fprm.nombre.data
        alum.apellidos=create_fprm.apellidos.data
        alum.email=create_fprm.email.data
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('alumnos.ABCompleto'))
    return render_template('modificar.html', form= create_fprm)


@alumnos.route("/eliminar",methods=['GET','POST'])
def eliminar():
    create_fprm=forms.UserForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        print('Esto es el id: ',id)
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_fprm.id.data=request.args.get('id')
        create_fprm.nombre.data=alum1.nombre
        create_fprm.apellidos.data=alum1.apellidos
        create_fprm.email.data=alum1.email
    if request.method=='POST':
        id=create_fprm.id.data
        alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.nombre=create_fprm.nombre.data
        alum.apellidos=create_fprm.apellidos.data
        alum.email=create_fprm.email.data
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for('alumnos.ABCompleto'))
    return render_template('eliminar.html', form= create_fprm)


@alumnos.route("/ABCompleto",methods=["GET","POST"])
def ABCompleto():
    create_form=forms.UserForm(request.form)
    alumno=Alumnos.query.all()
    print(alumno)
    return render_template("ABCompleto.html",form=create_form,alumno=alumno)
