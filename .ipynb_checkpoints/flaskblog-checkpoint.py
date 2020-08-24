from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect

app = Flask(__name__)


questions = [('What is your name?', ['Omar', 'Hazem', 'Mina', 'Noura'], ['d1', 'd2', 'd3', 'd4']),
         ('What is your age?', [19, 20, 21, 22], 'all_distractors',)
        ]
Qnums = len(questions)

@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', questions=questions, Qnums = Qnums)

@app.route('/qs')
def qs():
    return render_template('qs.html', questions=questions, Qnums = Qnums)


if __name__ == '__main__':
    app.run(debug=True)