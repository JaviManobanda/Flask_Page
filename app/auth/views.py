from flask import render_template,session, redirect, flash, url_for
from app.forms import LoginForm
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm()
    contexto = {
        'loginform': loginform
    }
    
    
    if loginform.validate_on_submit():
        username = loginform.username.data
        session['username'] = username
        flash('Nombre del usuario registrado con exito')
        return redirect(url_for('index'))

    return render_template('login.html', **contexto)
