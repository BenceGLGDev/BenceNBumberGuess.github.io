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
    data = request.get_json()
    if not data or 'guess' not in data:
        return jsonify({'message': 'Invalid input!'}), 400

    try:
        user_guess = int(data['guess'])
    except ValueError:
        return jsonify({'message': 'Please enter a valid number!'}), 400

    # Retrieve or initialize session variables
    secret_number = session.get('number', None)
    if secret_number is None:
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
