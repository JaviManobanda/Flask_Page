from flask import (Flask, request,
                   make_response, redirect,
                   render_template, session, url_for, flash)
import unittest
from app.forms import (LoginForm, TodoForm,
                       deleteTodoForm, updateForm)
from flask_login import login_required, current_user  # * require para el login

# * importamos bas de firestore
from app.firestore_service import (get_users, get_todos,
                                   put_todo, delete_todo,
                                   update_todo)
from app import create_app

app = create_app()  # ! Importa de create app

#* Este es el index de la app
@app.route('/')
def index():
    user_ip = request.remote_addr  #? Recibe la ip
    #? hacer un response y redirecciona
    response = make_response(redirect('/hello'))
    #? crea una cookie de la ip del usuario
    session['user_ip'] = user_ip
    return response


# * decorador que recibe la direccion a ejecutar
@app.route('/hello', methods=['GET','POST'])
@login_required  # * decorador de login
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()
    delete_form = deleteTodoForm()
    updateform = updateForm()
    ''' Creo instancia del form '''
    ctx = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'updateform':updateform
    }
    
    if todo_form.validate_on_submit():
        put_todo(username,todo_form.description.data)
        flash("La tarea se agregó con exito")
        return redirect(url_for('hello'))
    
    return render_template('hello.html', **ctx)

@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id,todo_id)
    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id,done):
    user_id = current_user.id
    update_todo(user_id,todo_id,done)
    return redirect(url_for('hello'))

''' Decoradoe de comandos '''
@app.cli.command() #* decorador para comandos cli de flask
def test():
    """ funtion to run tests
    """
    # * Busca el directorio con los test
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

''' errorHandler permite manejar el error '''
@app.errorhandler(500)
def not_Server(error):
    img = 'images/error500.png'
    message = 'Lo sentimos error con el servidor'
    return renderErrors(img, message, error)

@app.errorhandler(404)
def not_found(error):
    img = 'images/Scarecrow.png'
    message = 'Lo sentimos no encontramos lo que buscabas'
    return renderErrors(img, message, error)

def renderErrors(img, message, error):
    ctx = {'img': img,
           'message': message,
           'error': error
           }
    return render_template('Errors.html', **ctx)

@app.route('/error500')
def doError500():
    return ds


if __name__ == "__main__":
    app.run(debug=1,)
