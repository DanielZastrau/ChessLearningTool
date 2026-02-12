import json
import os
import random
import time

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


# Initialize global variables immediately
repertoire_white = load_repertoire('white')
repertoire_black = load_repertoire('black')
last_load = time.time()

lines_already_sent = set()


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


def get_random_line(tree_node) -> list[str]:
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


def get_next_move(moves: str, color: str):

    moves = moves.split(' ')

    if color == 'White':
        current_node = repertoire_white

    elif color == 'Black':
        current_node = repertoire_black

    for move in moves:

        if move in current_node:
            current_node = current_node[move]

        else:
            break

    return list(current_node.keys())


def replace_subtree_in_repertoire(move_list: list, color: str = 'white'):

    if color == 'white':
        current_node = repertoire_white
    elif color == 'black':
        current_node = repertoire_black

    for i, move in enumerate(move_list):

        if not move: 
            continue

        # In White Repertoire: Indices 0, 2, 4... (White's moves)
        # In Black Repertoire: Indices 1, 3, 5... (Black's moves)
        is_white_turn_in_game = (i % 2 == 0)
        
        if color == 'white':
            is_user_move = is_white_turn_in_game
        else:
            is_user_move = not is_white_turn_in_game

        # LOGIC: If it is User turn, they must only have ONE choice.
        if is_user_move:

            # If the repertoire already has a move here, and it is NOT the one I am playing now:
            # We must DELETE the old move (and its entire subtree) to replace it.
            if current_node and move not in current_node:
                current_node.clear()

        # LOGIC: If it is OPPONENT'S turn, they can have many moves.
        # We just add this one to the list of possibilities without deleting siblings.
        if move not in current_node:
            current_node[move] = {}
        
        current_node = current_node[move]


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

    global last_load, repertoire_black, repertoire_white

    if time.time() - last_load > 300:
        repertoire_white = load_repertoire('white')
        repertoire_black = load_repertoire('black')
        last_load = time.time()

        print("Repertoires reloaded from disk.")

    counter = 0
    while True:

        counter += 1

        if random.random() < 0.5:

            move_sequence = get_random_line(repertoire_white)
            color = 'white'
            breakpoint = random.randint(2, len(move_sequence) // 2 + 1)
            
        else:

            move_sequence = get_random_line(repertoire_black)
            color = 'black'
            breakpoint = random.randint(1, len(move_sequence) // 2)

        if str(move_sequence) not in lines_already_sent:
            lines_already_sent.add(str(move_sequence))
            
            return jsonify({
                'status': 200,
                'color': color,
                'move_sequence': move_sequence,
                'breakpoint': breakpoint
            })

        if counter == 200:
            
            return jsonify({
                'status': 500,
                'message': 'All lines quizzed.'
            })


@app.route('/get_next_moves', methods=['POST'])
def get_next_moves():

    global repertoire_black, repertoire_white

    data = request.json
    assert data and 'moves' in data and 'color' in data

    moves = data['moves']
    color = data['color']

    next_moves = get_next_move(moves, color)

    return jsonify({ 'status': 200, 'moves': next_moves })


@app.route('/update_subtree', methods=['POST'])
def update_subtree():
    
    data = request.json
    
    if not data or 'move sequence' not in data:
        return jsonify({
            'status': 400, 
            'message': 'No line provided'
        })

    raw_line = data.get('line', '').split(' ')
    color = data.get('color', 'white').lower()

    # Perform the update (Prune & Graft)
    replace_subtree_in_repertoire(raw_line, color)

    # Save immediately
    if color == 'white':
        save_repertoire(repertoire_white, 'white')
    elif color == 'black':
        save_repertoire(repertoire_black, 'black')

    return jsonify({ 
        'status': 200, 
        'message': 'Subtree updated successfully',
        'line': ' '.join([m for m in raw_line if m])
    })


if __name__ == '__main__':
    app.run(debug=True)