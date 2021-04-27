from flask_wtf import FlaskForm
# * Se importa los campos del formulario
from wtforms.fields import (StringField,
                            PasswordField,
                            SubmitField)
from wtforms.validators import DataRequired  # * se coloca validacion de datos


class LoginForm(FlaskForm):
    ''' Se crea los campos del formulario '''
    username = StringField('Nombre del usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')
class TodoForm(FlaskForm):
    description = StringField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Crear')
class deleteTodoForm(FlaskForm):
    submit = SubmitField('Borrar')
class updateForm(FlaskForm):
    submit = SubmitField('Actualizar')