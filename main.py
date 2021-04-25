from flask import (Flask, request,
                   make_response, redirect,
                   render_template, session, url_for, flash)
from flask_wtf import FlaskForm
import unittest
from app.forms import LoginForm

from flask_bootstrap import Bootstrap  # * para una mejor interfaz UI

from app import create_app

todos = ['Compar cafe', 'Imprimir piezas', 'Reunion de negocios']

app = create_app()  # ! Importa de create app

''' errorHandler permite manejar el error '''

''' Se crea una clase que extiendo de Flaskform '''


''' Decoradoe de comandos '''


@app.cli.command()
def test():
    """[summary]
    """
    # * Busca el directorio con los test
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


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


# decorador que recibe la direccion a ejecutar
@app.route('/hello', methods=['GET'])
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')
    ''' Creo instancia del form '''
    ctx = {
        'user_ip': user_ip,
        'todos': todos,
        'username': username
    }

    return render_template('hello.html', **ctx)


@app.route('/error500')
def doError500():
    return qwqwq


if __name__ == "__main__":
    app.run(debug=1,)
