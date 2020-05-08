from flask import Flask, jsonify, render_template

from cube.cube import Cube

cube = Cube()

app = Flask(__name__, template_folder='dist/templates',
            static_folder='dist/static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/get-cube')
def get_cube():
    return jsonify({'success': True, 'cube': cube.cube})


@app.route('/api/op/<op_name>')
def take_operate(op_name):
    if cube.take_action(op_name):
        return jsonify({'success': True, 'cube': cube.cube})
    return jsonify({'success': False, 'message': 'Bad operation'})


@app.route('/api/reset')
def reset():
    cube.reset()
    return jsonify({'success': True, 'cube': cube.cube})


@app.route('/api/go-back')
def go_back():
    if cube.go_back():
        return jsonify({'success': True, 'cube': cube.cube})
    else:
        return jsonify({'success': False, 'message': "Can't go back"})


@app.route('/api/shuffle')
def shuffle():
    cube.shuffle(20)
    return jsonify({'success': True, 'cube': cube.cube})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
