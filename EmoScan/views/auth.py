from flask import(
    render_template, Blueprint, flash, redirect, request, session, url_for
)

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from EmoScan.models.users import User
from EmoScan import db, app


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.getId(user_id)


auth = Blueprint('auth', __name__, )

#Registrar un usuario 
@auth.route('/registro', methods=('GET','POST'))
def registro():
    session.pop('show_table', None)
    session.pop('show_table2', None)
    if request.method == 'POST':

        # Obtener los datos del formulario de registro
        name = request.form.get('name')
        last = request.form.get('last')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hash_password = generate_password_hash(password)

        cursor = db.cursor()
        try:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            usuario_username = cursor.fetchone()
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            usuario_email = cursor.fetchone()

            if usuario_username is not None:
                error = 'El nombre de usuario ya está en uso'
                flash(error)
                
            elif usuario_email is not None:
                error = 'El correo electrónico ya está en uso'
                flash(error)
                
            else:
                # Insertar usuario en la base de datos
                cursor.execute('INSERT INTO users (name, last, username, email, password) VALUES (%s, %s, %s, %s, %s)',
                               (name, last, username, email, hash_password))
                db.commit()

                # Iniciar sesión
                cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                usuario = cursor.fetchone()
                id = usuario[0]
                user = User(id, name, last, username, email, hash_password)
                login_user(user)

                return redirect(url_for('principal'))
        except Exception as e:
            print(e)
            error = 'Error en el registro, inténtelo de nuevo'
            flash(error)
            return render_template('auth/registro.html')

    return render_template('auth/registro.html')
    

@auth.route('/login', methods=('GET','POST'))
def login():
    session.pop('show_table', None)
    session.pop('show_table2', None)
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

    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('index'))


@auth.route('/delete_account', methods=('GET', 'POST'))
@login_required
def delete_account():
    if request.method == 'POST':
        # Obtener la contraseña ingresada por el usuario
        password = request.form['password']

        # Verificar si la contraseña es válida para el usuario actual
        if check_password_hash(current_user.password, password):
            # Eliminar la cuenta del usuario actual de la base de datos
            session.clear()
            cursor = db.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s", (current_user.id,))
            db.commit()

            # Cerrar la sesión del usuario
            logout_user()

            # Redireccionar a la página de inicio o a cualquier otra página deseada
            return redirect(url_for('index'))
        else:
            # Contraseña incorrecta, mostrar un mensaje de error o realizar otra acción apropiada
            flash('Contraseña incorrecta. No se pudo eliminar la cuenta.', 'error')

    # Si se accede a la ruta con el método GET, mostrar un error o redireccionar
    return redirect(url_for('perfil'))


@auth.route('/perfil', methods=('GET', 'POST'))
@login_required
def perfil():
    session.pop('show_table', None)
    session.pop('show_table2', None)

    if request.method == 'POST':
        name = request.form.get('name')
        last = request.form.get('last')
        username = request.form.get('username')
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')

        if name or last:
        # Actualizar nombre y/o apellido en la base de datos
            if name and last:
                # Actualizar ambos campos
                User.updateUserData(current_user.id, 'name', name)
                User.updateUserData(current_user.id, 'last', last)
                flash('Nombre y apellido actualizados correctamente.', 'success')
            elif name:
                # Actualizar solo el nombre
                User.updateUserData(current_user.id, 'name', name)
                flash('Nombre actualizado correctamente.', 'success')
            elif last:
                # Actualizar solo el apellido
                User.updateUserData(current_user.id, 'last', last)
                flash('Apellido actualizado correctamente.', 'success')

        if username:
            # Actualizar nombre de usuario en la base de datos
            User.updateUserData(current_user.id,'username', username)
            flash('Nombre de usuario actualizado correctamente.', 'success')

        if email:
            # Actualizar correo electrónico en la base de datos
            User.updateUserData(current_user.id,'email', email)
            flash('Correo electrónico actualizado correctamente.', 'success')

        if current_password and new_password:
            # Verificar la contraseña actual y actualizar la contraseña en la base de datos
            cursor = db.cursor()
            sql = "SELECT password FROM users WHERE id = %s"
            cursor.execute(sql, (current_user.id,))
            result = cursor.fetchone()

            if result and check_password_hash(result[0], current_password):
                hashed_password = generate_password_hash(new_password)
                User.updateUserData(current_user.id,'password', hashed_password)
                flash('Contraseña actualizada correctamente.', 'success')
            else:
                flash('La contraseña actual no es correcta.', 'error')

        return redirect(url_for('auth.perfil'))


    return render_template('auth/perfil.html')