from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'clave_secreta' 

@app.route('/', methods=['GET', 'POST'])
def juego():
    color = ""

    if 'numero_secreto' not in session or'reinicio' in request.form:
        session['numero_secreto'] = random.randint(1, 100)
        print(session['numero_secreto'])
        session['intentos'] = 0

    if 'ganadores' not in session:
        session['ganadores'] = []

    if request.method == 'POST':
        intento = request.form.get('intento', type=int)
        if intento is not None:
            session['intentos'] += 1

            if intento < session['numero_secreto']:
                mensaje = "Demasiado bajo"
                color = "#F05131"
            elif intento > session['numero_secreto']:
                mensaje = "Demasiado alto"
                color = "#F05131"
            else:
                mensaje = "¡Correcto!"
                color = "green"
                return redirect('/ganador')
        else:
            mensaje = "¡Adivina el número!"

    else:
        mensaje = "¡Adivina el número!"

    if session['intentos'] >= 5:
        mensaje = "¡Tú pierdes!"
        color = "#F05131"
        session.pop('numero_secreto')
        session.pop('intentos')

    return render_template('juego.html', mensaje=mensaje, color=color, ganadores=session['ganadores'])

@app.route('/ganador', methods=['GET', 'POST'])
def ganador():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ganadores = session.get('ganadores', []) 
        ganadores.append({'nombre': nombre, 'intentos': session['intentos']})
        session['ganadores'] = ganadores
        session.pop('numero_secreto')
        session.pop('intentos')
        return redirect('/')

    return render_template('ganador.html', ganadores=session.get('ganadores', []))


if __name__ == '__main__':
    app.run(debug=True)
