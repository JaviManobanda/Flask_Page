from flask import (Flask,
                   request, make_response,
                   redirect, render_template)


todos = ['Compar cafe', 'Imprimir piezas', 'Reunion de negocios']

app = Flask(__name__)  # crea instancia de flask
""" Debes pasar el nombre de la aplicación """

''' errorHandler permite manejar el error '''
@app.errorhandler(404)
def not_found(error):
    img = 'images/Scarecrow.png'
    message = 'Lo sentimos no encontramos lo que buscabas'
    return renderErrors(img,message,error)
    
@app.errorhandler(500)
def not_Server(error):
    img = 'images/error500.png'
    message = 'Lo sentimos error con el servidor'
    return renderErrors(img,message,error)


def renderErrors(img,message,error):
    ctx ={'img':img,
          'message': message,
          'error':error
          }
    return render_template('Errors.html', **ctx)


@app.route('/')
def index():
    user_ip = request.remote_addr  # Recibe la ip
    # hacer un response y redirecciona
    response = make_response(redirect('/hello'))
    # crea una cookie de la ip del usuario
    response.set_cookie('user_ip', user_ip)

    return response


@app.route('/hello')  # decorador que recibe la direccion a ejecutar
def hello():
    user_ip = request.cookies.get('user_ip')
    # renderizo el tempate
    ctx = {
        'user_ip': user_ip,
        'todos': todos
    }
    return render_template('hello.html', **ctx)
    # y envio la ip

@app.route('/error500')
def doError500():
    return qwqwq

if __name__ == "__main__":
    app.run(debug=0)
