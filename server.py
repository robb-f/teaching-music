# Chidi Azuike       - ca2970
# Robert Fornos      - rf2830
# Shreya Somayajula  - svs2137
# Vaibhav Sourirajan - vs2787

from flask import Flask, render_template, Response, request, jsonify, redirect, url_for

app = Flask(__name__)

# GLOBAL VARIABLES

# ROUTES

# Home
@app.route('/')
def home():
    return render_template('home.html')

# Learn (static)
@app.route('/learn')
def learn():
    return redirect(url_for('learn_lesson', lesson_number=1))

# Learn (dynamic - with lesson number)
@app.route('/learn/<int:lesson_number>')
def learn_lesson(lesson_number):
    return render_template('learn.html', lesson_number=lesson_number)

# Quiz
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

# AJAX FUNCTIONS

if __name__ == '__main__':
    app.run(debug=True, port=5001)
