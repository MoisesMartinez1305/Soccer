import os 
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)   
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Jugador(db.Model):
    __tablename__ = 'jugadores'
    Dorsal = db.Column(db.String, primary_key=True)
    Nombre = db.Column(db.String, nullable=True)
    Ap_paterno = db.Column(db.String, nullable=True)
    Ap_materno = db.Column(db.String, nullable=True)
    Edad_en_años = db.Column(db.Integer, nullable=True)
    Equipo = db.Column(db.String, nullable=True)

    def to_dict(self):
        return {
            'Dorsal': self.Dorsal,
            'Nombre': self.Nombre,
            'Ap_paterno': self.Ap_paterno,
            'Ap_materno': self.Ap_materno,
            'Edad_en_años': self.Edad_en_años,
            'Equipo': self.Equipo,
        }

# Ruta principal
@app.route('/')
def index():
    jugadores = Jugador.query.all()  # Cambiado de alumnos a jugadores
    return render_template('index.html', jugadores=jugadores)  # Variable modificada

# Ruta para crear jugadores
@app.route('/jugadores/new', methods=['GET', 'POST'])  # Ruta modificada
def create_jugador():  # Nombre de función cambiado
    if request.method == 'POST':
        nuevo_jugador = Jugador(
            Dorsal=request.form['Dorsal'],
            Nombre=request.form['Nombre'],
            Ap_paterno=request.form['Ap_paterno'],
            Ap_materno=request.form['Ap_materno'],
            Edad_en_años=request.form['Edad_en_años'],
            Equipo=request.form['Equipo']
        )
        
        db.session.add(nuevo_jugador)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('create_jugador.html')  # Plantilla modificada

# Ruta para eliminar jugadores
@app.route('/jugadores/delete/<string:Dorsal>')  # Ruta modificada
def delete_jugador(Dorsal):  # Nombre de función cambiado
    jugador = Jugador.query.get(Dorsal)  # Cambiado de Alumno a Jugador
    if jugador:
        db.session.delete(jugador)
        db.session.commit()
    return redirect(url_for('index'))

# Ruta para actualizar jugadores
@app.route('/jugadores/update/<string:Dorsal>', methods=['GET', 'POST'])  # Ruta modificada
def update_jugador(Dorsal):  # Nombre de función cambiado
    jugador = Jugador.query.get(Dorsal)  # Cambiado de Alumno a Jugador
    if request.method == 'POST':
        jugador.Nombre = request.form['Nombre']
        jugador.Ap_paterno = request.form['Ap_paterno']
        jugador.Ap_materno = request.form['Ap_materno']
        jugador.Edad_en_años = request.form['Edad_en_años']
        jugador.Equipo = request.form['Equipo']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_jugador.html', jugador=jugador)  # Plantilla modificada

if __name__ == '__main__':
    app.run(debug=True)