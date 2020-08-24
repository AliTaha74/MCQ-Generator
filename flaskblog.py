from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import redirect
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import validators
from wtforms.fields.html5 import EmailField
from Flask_Blog import NLPMethods


import self as self


app = Flask(__name__)

app.config['SECRET_KEY'] = 'e0c85d87936c3e992762ae6719abadac'
'''
questions = [('what is your name', ['Omar', 'Hazem', 'Mina', 'Noura'], ['d1', 'd2', 'd3', 'd4']),
         ('What is your age?', [19, 20, 21, 22], 'all_distractors',)
        ]
'''
questions2 = []
Qnums = 100

#p = ""

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', questions=questions2, Qnums = Qnums)

@app.route('/qs')
def qs():
    return render_template('qs.html', questions=questions2, Qnums = Qnums)

@app.route('/', methods=['GET', 'POST'])
def txt():
    r = request
    if r.method == 'GET':
        return render_template('home.html')
    if r.method == 'POST':
        p = r.form['paragraph']
        questions2 = NLPMethods.test(p)
        Qnums =len(questions2)
        return render_template('qs.html', questions=questions2, Qnums=Qnums, )



if __name__ == '__main__':
    app.run(debug=True)


