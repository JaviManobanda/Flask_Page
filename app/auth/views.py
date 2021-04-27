from flask import render_template,session, redirect, flash, url_for
from flask_login import login_user, login_required,logout_user
from werkzeug import generate_password_hash, check_password_hash
from app.forms import LoginForm
from . import auth
from app.firestore_service import get_user, user_put
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
            if check_password_hash(password_from_db, password):
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

@auth.route('signup',methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    ctx = {
        'signup_form': signup_form,
    }
    
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        user_doc = get_user(username)
        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username,password_hash)
            user_put(user_data)
            user = UserModel(user_data)
            login_user(user)
            flash('Bienvenido!')
            return redirect(url_for('hello'))
        else:
            flash('El usuario ya existe')
    return render_template('signup.html', **ctx)

@auth.route('logout')
@login_required
def logout():
    flash('Regresa pronto')
    logout_user() #nomandas parametro
    return redirect(url_for('auth.login'))


