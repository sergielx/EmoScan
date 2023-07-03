from flask import(
    render_template, Blueprint, flash,request
)

from flask_mail import Mail, Message
from EmoScan import app

contact = Blueprint('contact', __name__, )

mail = Mail(app)

@contact.route('/contacto', methods=('GET','POST'))
def contacto():
    if request.method == 'POST':
        email = request.form['email']
        mensaje = request.form['mensaje']
        mensaje_enviado = None
        try:
            msg = Message(mensaje, sender="emoscantfg@gmail.com", recipients=[email])
            msg.body = "Prueba"
            msg.html = "<b>Prueba</b>"
            mail.send(msg)
            mensaje_enviado = "El mensaje se ha enviado con éxito"
            flash(mensaje_enviado)
        except Exception as e:
            mensaje_error = "Hubo un problema al enviar el mensaje: {}".format(str(e))
            flash(mensaje_error, category='error')
    return render_template('enlaces_rapidos/contacto.html')

