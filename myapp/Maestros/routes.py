from flask import Blueprint, render_template, redirect, url_for, request, flash
from db import get_connection
from models import db
from models import Maestros
import forms

maestros= Blueprint('maestros', __name__)


@maestros.route("/insertarMaestro",methods=['GET', 'POST'])
def index():
    create_form=forms.MaestroForm(request.form)
    if request.method == 'POST':
        nombre = create_form.nombre.data
        apellidos = create_form.apellidos.data
        email = create_form.email.data
        profesion = create_form.profesion.data

        try:
           connection=get_connection()
           with connection.cursor() as cursor:
                cursor.execute('call insertar_maestro(%s,%s,%s,%s)', (nombre, apellidos, email, profesion))
           connection.commit()
           connection.close()
           flash('Se inserto Correctamente!')

        except Exception as ex:
            print('ERROR {}'.format(ex))

        # Redirige al usuario a la vista ABCompleto
        return redirect(url_for('maestros.ABCompleto'))
    
    return render_template('indexMaestro.html',form=create_form)
    

@maestros.route("/modificarMaestro",methods=['GET','POST'])
def modificar():
    create_fprm=forms.MaestroForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        connection = get_connection()
        try:
           with connection.cursor() as cursor:
               cursor.execute('CALL mostrarUnMaestro(%s)',(id))
               resultset = cursor.fetchall()
           create_fprm.id.data=request.args.get('id')
           create_fprm.nombre.data=resultset[0][1]
           create_fprm.apellidos.data=resultset[0][2]
           create_fprm.email.data=resultset[0][3]
           create_fprm.profesion.data=resultset[0][4]           
        except Exception as ex:
           print(ex)
        finally:
           connection.close()

    if request.method=='POST':
        id=create_fprm.id.data
        nombre = create_fprm.nombre.data
        apellidos = create_fprm.apellidos.data
        email = create_fprm.email.data
        profesion = create_fprm.profesion.data
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('CALL actualizar_maestro(%s,%s,%s,%s,%s)', (id, nombre, apellidos, email, profesion))
            connection.commit()
            connection.close()
            flash('El registro con nombre {} se modifico correctamente!'.format(nombre))

        except Exception as ex:
           print('ERROR {}'.format(ex))
        return redirect(url_for('maestros.ABCompleto'))
    return render_template('modificarMaestro.html', form= create_fprm)


@maestros.route("/eliminarMaestro",methods=['GET','POST'])
def eliminar():
    create_fprm=forms.MaestroForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        connection = get_connection()
        try:
           with connection.cursor() as cursor:
               cursor.execute('CALL mostrarUnMaestro(%s)',(id))
               resultset = cursor.fetchall()
           create_fprm.id.data=request.args.get('id')
           create_fprm.nombre.data=resultset[0][1]
           create_fprm.apellidos.data=resultset[0][2]
           create_fprm.email.data=resultset[0][3]
           create_fprm.profesion.data=resultset[0][4]           
        except Exception as ex:
           print(ex)
        finally:
           connection.close()
    if request.method=='POST':
        id=create_fprm.id.data
        try:
            connection=get_connection()
            with connection.cursor() as cursor:
                cursor.execute('CALL eliminar_maestro(%s)', (id))
            connection.commit()
            connection.close()

        except Exception as ex:
           print('ERROR {}'.format(ex))
        return redirect(url_for('maestros.ABCompleto'))
    return render_template('eliminarMaestro.html', form= create_fprm)


@maestros.route("/ABCompletoMaestro",methods=["GET","POST"])
def ABCompleto():
    create_form=forms.MaestroForm(request.form)
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('call mostrarTodosMaestro()')
            resultset = cursor.fetchall()
    except Exception as ex:
        print(ex)
    finally:
        connection.close()
    print (resultset)
    return render_template("ABCompletoMaestro.html", form=create_form, resultset=resultset)
