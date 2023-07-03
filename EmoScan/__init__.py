from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from flask_login import login_user, login_required, current_user
from werkzeug.security import check_password_hash

app = Flask(__name__)


app.config.from_object('config.DevelopmentConfig')
app.secret_key = 'dev'


# Configuración del correo electrónico
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'emoscantfg@gmail.com'
app.config['MAIL_PASSWORD'] = 'rlhlwiamildupzpx'
app.config['MAIL_DEFAULT_SENDER'] = 'emoscantfg@gmail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['TESTING'] = False

#Configuración de la base de datos
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="emoscan_db"
)


# #Importar vistas 
from EmoScan.views.auth import auth
from EmoScan.views.contacto import contact
from EmoScan.views.buscar import busc
from EmoScan.views.analizar import ana
from EmoScan.views.estadisticas import est
app.register_blueprint(auth)
app.register_blueprint(contact)
app.register_blueprint(busc)
app.register_blueprint(ana)
app.register_blueprint(est)



from EmoScan.models.users import User
@app.route('/', methods=['GET', 'POST'])
def index():

    if current_user.is_authenticated:
        return redirect(url_for('principal'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = db.cursor()

        try:
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            if user is None:
                # Si el usuario no existe
                flash('Correo electrónico o contraseña incorrectos', 'error')     
            elif not check_password_hash(user[5], password):
                # Si la contraseña es incorrecta
                flash('Correo electrónico o contraseña incorrectos', 'error') 
                           
            else:
                # Si todo es correcto
                user_obj = User(user[0], user[1], user[2], user[3], user[4], user[5])
                login_user(user_obj)
                return redirect(url_for('principal'))
        except Exception as e:
            print(e)
            flash('Error en el inicio de sesión, inténtalo de nuevo', 'error')
    return render_template('index.html')


#Configuración de las páginas de Enlaces rápidos
@app.route('/quienes_somos')
def quienes_somos():
    session.pop('show_table', None)
    session.pop('show_table2', None)
    return render_template('enlaces_rapidos/quienes_somos.html')

@app.route('/politica_privacidad')
def politica_privacidad():
    session.pop('show_table', None)
    session.pop('show_table2', None)
    return render_template('enlaces_rapidos/politica_privacidad.html')

@app.route('/terminos_condiciones')
def terminos_condiciones():
    session.pop('show_table', None)
    session.pop('show_table2', None)
    return render_template('enlaces_rapidos/terminos_condiciones.html')

@app.route('/principal')
@login_required
def principal():
    session.pop('show_table', None)
    session.pop('show_table2', None)
    return render_template('principal.html')

#Configuración de las páginas de error.
def status_401(error):
    session.pop('show_table', None)
    session.pop('show_table2', None)
    return redirect(url_for('index'))


def status_404(error):
    session.pop('show_table', None)
    session.pop('show_table2', None)
    return render_template('errores/error404.html'), 404

def status_403(error):
    session.pop('show_table', None)
    session.pop('show_table2', None)
    return render_template('errores/error403.html'), 403



app.register_error_handler(401, status_401)
app.register_error_handler(404, status_404)
app.register_error_handler(403, status_403)




