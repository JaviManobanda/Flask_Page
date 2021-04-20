from flask import (Flask, request,
                   make_response, redirect,
                   render_template, session,url_for,flash)
from flask_wtf import FlaskForm
import unittest

# * Se importa los campos del formulario
from wtforms.fields import (StringField,
                            PasswordField,
                            SubmitField)
from wtforms.validators import DataRequired  # * se coloca validacion de datos
from flask_bootstrap import Bootstrap  # * para una mejor interfaz UI


todos = ['Compar cafe', 'Imprimir piezas', 'Reunion de negocios']

app = Flask(__name__)  # ! crea instancia de flask
app.config['SECRET_KEY'] = 'SUPER SECRETO'

""" Debes pasar el nombre de la aplicación """
''' Instanciamos bootstrap '''
bootstrap = Bootstrap(app)

''' errorHandler permite manejar el error '''

''' Se crea una clase que extiendo de Flaskform '''


class LoginForm(FlaskForm):
    ''' Se crea los campos del formulario '''
    username = StringField('Nombre del usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

''' Decoradoe de comandos '''
@app.cli.command()
def test():
    """[summary]
    """
    #* Busca el directorio con los test
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


@app.route('/hello',methods=['GET','POST'])  # decorador que recibe la direccion a ejecutar
def hello():
    ''' user_ip = request.cookies.get('user_ip') '''
    user_ip = session.get('user_ip')
    username = session.get('username')
    ''' Creo instancia del form '''
    loginform = LoginForm()
    # renderizo el tempate
    ctx = {
        'user_ip': user_ip,
        'todos': todos,
        'loginform': loginform,
        'username':username
    }
    
    ''' oBTENER DATOS DE LA FORMA '''
    if loginform.validate_on_submit():
        username = loginform.username.data
        session['username'] = username
        flash('Nombre del usuario registrado con exito')
        return redirect(url_for('index'))
        
    return render_template('hello.html', **ctx)
    # y envio la ip


@app.route('/error500')
def doError500():
    return qwqwq


if __name__ == "__main__":
    app.run(debug=1,)
