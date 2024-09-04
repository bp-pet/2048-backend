from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ts = db.Column(db.DateTime, server_default=db.func.now())
    name = db.Column(db.String(50), nullable=False)
    scored_points = db.Column(db.Integer, nullable=False)
    board_x = db.Column(db.Integer, nullable=False)
    board_y = db.Column(db.Integer, nullable=False)

@app.route('/<int:board_x>/<int:board_y>', methods=['GET'])
def get_scores(board_x, board_y):
    """Get all scores for a specific board size in descending order"""
    scores = Score.query.all()
    filtered_scores = [score for score in scores if score.board_x == board_x and score.board_y == board_y]
    filtered_scores.sort(key=lambda score: score.scored_points, reverse=True)
    final_list = [{'name': score.name, 'points': score.scored_points} for score in filtered_scores]
    return jsonify({'scores': final_list})


@app.route('/', methods=['POST'])
def add_score():
    new_score = Score(name=request.json['name'], scored_points=request.json['points'], board_x=request.json['board_x'], board_y=request.json['board_y'])

    with app.app_context():
        db.session.add(new_score)
        db.session.commit()

    return jsonify({'message': 'Score added successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)