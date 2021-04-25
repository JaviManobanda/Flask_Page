from flask import render_template,session, redirect, flash, url_for
from flask_login import login_user, login_required,logout_user
from app.forms import LoginForm
from . import auth
from app.firestore_service import get_user
from app.models import UserData, UserModel

@auth.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    contexto = {
        'loginform': loginform
    }

    if loginform.validate_on_submit():
        #* valida que el usuario este en la bd
        username = loginform.username.data
        password = loginform.password.data
        user_doc = get_user(username)
        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']
            if password == password_from_db:
                user_data = UserData(username,password)
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido de nuevo')
                redirect(url_for('hello'))
            else:
                flash('La información es incorrecta')
        else:
            flash('El usuario no existe')

        return redirect(url_for('index'))

    return render_template('login.html', **contexto)

@auth.route('logout')
@login_required
def logout():
    flash('Regresa pronto')
    logout_user() #nomandas parametro
    return redirect(url_for('auth.login'))