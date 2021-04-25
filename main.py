from flask import (Flask, request,
                   make_response, redirect,
                   render_template, session, url_for, flash)
import unittest
from app.forms import LoginForm
from flask_login import login_required, current_user #* require para el login

#* importamos bas de firestore
from app.firestore_service import get_users, get_todos
from app import create_app

app = create_app()  # ! Importa de create app

''' Decoradoe de comandos '''
@app.cli.command()
def test():
    """[summary]
    """
    # * Busca el directorio con los test
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


''' errorHandler permite manejar el error '''
@app.errorhandler(404)
def not_found(error):
    img = 'images/Scarecrow.png'
    message = 'Lo sentimos no encontramos lo que buscabas'
    return renderErrors(img, message, error)


@app.errorhandler(500)
def not_Server(error):
    img = 'images/error500.png'
    message = 'Lo sentimos error con el servidor'
    return renderErrors(img, message, error)


def renderErrors(img, message, error):
    ctx = {'img': img,
           'message': message,
           'error': error
           }
    return render_template('Errors.html', **ctx)


@app.route('/')
def index():
    user_ip = request.remote_addr  # Recibe la ip
    # hacer un response y redirecciona
    response = make_response(redirect('/hello'))
    # crea una cookie de la ip del usuario
    ''' response.set_cookie('user_ip', user_ip) '''
    session['user_ip'] = user_ip

    return response


#* decorador que recibe la direccion a ejecutar
@app.route('/hello', methods=['GET'])
@login_required #* decorador de login
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    ''' Creo instancia del form '''
    ctx = {
        'user_ip': user_ip,
        'todos': get_todos(user_id = username),
        'username': username
    }
    
    return render_template('hello.html', **ctx)


@app.route('/error500')
def doError500():
    return qwqwq


if __name__ == "__main__":
    app.run(debug=1,)
