# app.py
from flask import Flask, render_template, request, session
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')


@app.route('/', methods=['GET', 'POST'])
def game():
    if 'number' not in session:
        session['number'] = random.randint(1, 100)
        session['attempts'] = 0
        session['message'] = "I'm thinking of a number between 1 and 100."

    if request.method == 'POST':
        try:
            guess = int(request.form['guess'])
            session['attempts'] += 1

            if guess < session['number']:
                session['message'] = f"Too low! Try a higher number. Attempts: {session['attempts']}"
            elif guess > session['number']:
                session['message'] = f"Too high! Try a lower number. Attempts: {session['attempts']}"
            else:
                session['message'] = f"Congratulations! You got it in {session['attempts']} attempts!"
                session.pop('number')
        except ValueError:
            session['message'] = "Please enter a valid number!"

    return render_template('game.html', message=session.get('message'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))