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
with app.app_context():
	db.create_all()
    
@app.route('/')
def index():
    jugadores = Jugador.query.all()
    return render_template('index.html', jugadores=jugadores)

@app.route('/jugadores/new', methods=['GET', 'POST'])
def create_jugador():
    if request.method == 'POST':
        dorsal = request.form['Dorsal']
        nombre = request.form['Nombre']
        ap_paterno = request.form['Ap_paterno']
        ap_materno = request.form['Ap_materno']
        edad_en_años = request.form['Edad_en_años']
        equipo = request.form['Equipo']

        existing_jugador = Jugador.query.filter_by(Dorsal=dorsal).first()
        if existing_jugador:
            return render_template('create_jugador.html', error_message="Ya existe un jugador con ese dorsal. Por favor, elige otro.")

        nuevo_jugador = Jugador(
            Dorsal=dorsal,
            Nombre=nombre,
            Ap_paterno=ap_paterno,
            Ap_materno=ap_materno,
            Edad_en_años=edad_en_años,
            Equipo=equipo
        )
        db.session.add(nuevo_jugador)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create_jugador.html')

@app.route('/jugadores/delete/<string:Dorsal>')
def delete_jugador(Dorsal):
    jugador = Jugador.query.get(Dorsal)
    if jugador:
        db.session.delete(jugador)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/jugadores/update/<string:Dorsal>', methods=['GET', 'POST'])
def update_jugador(Dorsal):
    jugador = Jugador.query.get(Dorsal)
    if request.method == 'POST':
        jugador.Nombre = request.form['Nombre']
        jugador.Ap_paterno = request.form['Ap_paterno']
        jugador.Ap_materno = request.form['Ap_materno']
        jugador.Edad_en_años = request.form['Edad_en_años']
        jugador.Equipo = request.form['Equipo']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_jugador.html', jugador=jugador)

if __name__ == '__main__':
    app.run(debug=True)