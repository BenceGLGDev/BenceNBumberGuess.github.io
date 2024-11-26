from flask import Flask, request, jsonify, send_file, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    # Serve the HTML file
    return send_file('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    user_guess = int(request.json.get('guess'))
    secret_number = session.get('number', None)
    
    # Start a new game if not already started
    if not secret_number:
        session['number'] = random.randint(1, 100)
        session['attempts'] = 0
        secret_number = session['number']

    session['attempts'] += 1

    if user_guess < secret_number:
        return jsonify({'message': 'Too low!'})
    elif user_guess > secret_number:
        return jsonify({'message': 'Too high!'})
    else:
        attempts = session['attempts']
        session.pop('number', None)  # Reset the game
        session.pop('attempts', None)
        return jsonify({'message': f'Correct! You guessed it in {attempts} attempts.'})

if __name__ == '__main__':
    app.run(debug=True)
