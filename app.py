from flask import *
from boggle import Boggle



app = Flask(__name__)
app.config['SECRET_KEY'] = 'be quiet'



boggle_game = Boggle()


@app.route("/")
def show_boggle_board():
    """shows boggle board with form to guess words"""

    board = boggle_game.make_board()
    session["board"] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template('boggle.html', board=board, 
                           highscore=highscore,
                           nplays=nplays)


@app.route("/word-check")
def get_word():
    """Check if word is valid or not"""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)