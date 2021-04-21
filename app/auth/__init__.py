from flask import Blueprint

# * Todas las rutas que tengan /auth van a ser ruteadas
auth = Blueprint('auth', __name__, url_prefix='/auth')

#! se importa despues el orden importa
from . import views