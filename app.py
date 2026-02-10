import json
import os
import random

from flask import Flask, render_template, request, jsonify
import chess

app = Flask(__name__)


def load_repertoire(color):

    if color == 'white':
        data_file = 'repertoire_white.json'
    elif color == 'black':
        data_file = 'repertoire_black.json'

    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return {}


def save_repertoire(data, color):
    if color == 'white':
        data_file = 'repertoire_white.json'
    elif color == 'black':
        data_file = 'repertoire_black.json'
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)


# Initialize global variable immediately
repertoire_white = load_repertoire('white')
repertoire_black = load_repertoire('black')

def add_line_to_repertoire(move_list: list, color: str = 'white'):

    # pointer
    if color == 'white':
        current_node = repertoire_white
    elif color == 'black':
        current_node = repertoire_black

    for move in move_list:
        
        # Clean up input (remove empty strings from double spaces)
        if not move: 
            continue
            
        if move not in current_node:
            current_node[move] = {}
        
        # Move the pointer down
        current_node = current_node[move]


def get_random_line(tree_node):
    """
    Walks from the root of the tree to a leaf node by choosing
    random branches at every step.
    """
    line = []
    current_node = tree_node
    
    while current_node:
        possible_moves = list(current_node.keys())
        
        # If we hit a leaf (no children), stop
        if not possible_moves:
            break
            
        # Pick a random move
        move = random.choice(possible_moves)
        line.append(move)
        
        # Step down
        current_node = current_node[move]
        
    return line


# Routes

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save_line', methods=['POST'])
def save_line():
    data = request.json
    
    # Basic validation
    if not data or 'line' not in data:
        return jsonify({'status': 400, 'message': 'No line provided'})

    raw_line = data.get('line', '').split(' ')
    color = data.get('color', 'white').lower()

    # Add to memory
    add_line_to_repertoire(raw_line, color)
    if color == 'white':
        save_repertoire(repertoire_white, 'white')
    elif color == 'black':
        save_repertoire(repertoire_black, 'black')

    # --- Formatting for the user response (Visual only) ---
    formatted_line = []
    move_number = 1
    
    clean_moves = [m for m in raw_line if m]
    
    for i in range(0, len(clean_moves), 2):

        white = clean_moves[i]

        # Check if there is a black move
        black = clean_moves[i+1] if (i + 1) < len(clean_moves) else ""
        
        if black:
            formatted_line.append(f"{move_number}. {white} {black}")
        else:
            formatted_line.append(f"{move_number}. {white}")
        move_number += 1

    return jsonify({ 
        'status': 200, 
        'line': ' '.join(formatted_line) 
    })

@app.route('/get_move_sequence', methods=['GET'])
def get_move_sequence():

    if random.random() < 0.5:
        move_sequence = get_random_line(repertoire_white)

        return jsonify({
            'status': 200,
            'color': 'white',
            'move_sequence': move_sequence,
            'breakpoint': random.randint(2, len(move_sequence) // 2 + 1)
        })

    else:
        move_sequence = get_random_line(repertoire_black)
        return jsonify({
            'status': 200,
            'color': 'black',
            'move_sequence': move_sequence,
            'breakpoint': random.randint(1, len(move_sequence) // 2)
        })


if __name__ == '__main__':
    app.run(debug=True)