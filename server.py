# Chidi Azuike       - ca2970
# Robert Fornos      - rf2830
# Shreya Somayajula  - svs2137
# Vaibhav Sourirajan - vs2787

from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
import data as app_data

app = Flask(__name__)


quiz_started = False
data = app_data.app_data

# GLOBAL VARIABLES

cur_lesson = 1
lesson = {
    1: {
        'genre': 'Medieval',
        'composer': 'Hildegard von Bingen',
        'piece': 'Columba Aspexit',
        'link': 'https://www.youtube.com/watch?v=BpmMeIQywYc'
    },
    2: {
        'genre': 'Medieval',
        'composer': 'Gregorian Chant',
        'piece': 'Deum vera',
        'link': 'https://www.youtube.com/watch?v=kK5AohCMX0U'
    },
    3: {
        'genre': 'Renaissance',
        'composer': 'Josquin des Prez',
        'piece': 'Ave Maria',
        'link': 'https://www.youtube.com/watch?v=xGkb5KFwx1I'
    },
    4: {
        'genre': 'Renaissance',
        'composer': 'Carlo Gesualdo',
        'piece': 'Moro Lasso',
        'link': 'https://www.youtube.com/watch?v=xGkb5KFwx1I'
    },
    5: {
        'genre': 'Baroque',
        'composer': 'J.S. Bach',
        'piece': 'Harpsichord Concerto No. 1',
        'link': 'https://www.youtube.com/watch?v=XcsfDxojdV8'
    },
    6: {
        'genre': 'Baroque',
        'composer': 'G.F. Handel',
        'piece': 'Julius Caesar, Act II',
        'link': 'https://www.youtube.com/watch?v=ppAUohisvG8'
    },
    7: {
        'genre': 'Classical',
        'composer': 'W.A. Mozart',
        'piece': 'Impresario Overture',
        'link': 'https://www.youtube.com/watch?v=7vaBubCmhWA'
    },
    8: {
        'genre': 'Classical',
        'composer': 'Chevalier de Saint-Georges',
        'piece': 'Violin Concerto in A Major',
        'link': 'https://www.youtube.com/watch?v=eQ1unCtX6K0'
    },
    9: {
        'genre': 'Romantic',
        'composer': 'Anton von Bruckner',
        'piece': 'Symphony No. 7',
        'link': 'https://www.youtube.com/watch?v=dSGOaTuAesY&t=528s'
    },
    10: {
        'genre': 'Romantic',
        'composer': 'Ludwig van Beethoven',
        'piece': 'Symphony No. 5',
        'link': 'https://www.youtube.com/watch?v=yKl4T5BnhOA'
    },
    11: {
        'genre': 'Modern/Contemporary',
        'composer': 'Igor Stravinsky',
        'piece': 'The Rite of Spring',
        'link': 'https://www.youtube.com/watch?v=EkwqPJZe8ms'
    },
    12: {
        'genre': 'Modern/Contemporary',
        'composer': 'Krzysztof Penderecki',
        'piece': 'Threnody to the Victims of Hiroshima',
        'link': 'https://www.youtube.com/watch?v=HilGthRhwP8'
    }
}

# ROUTES

# Home
@app.route('/')
def home():
    return render_template('home.html')

# Learn (static)
@app.route('/learn')
def learn():
    return redirect(url_for('learn_lesson', lesson_number=1))

@app.route('/learn/<int:lesson_number>')
def learn_lesson(lesson_number):
    return render_template('learn.html', lesson_number=lesson_number, lesson=lesson)

# Quiz
# @app.route('/quiz')
# def quiz():
#     return render_template('quiz.html')

@app.route('/quiz/<int:quiz_num>/')
def quiz(quiz_num):
    global quiz_started
    
    if quiz_started:
        question = data["quizzes"][quiz_num - 1]
    else:
        question = data["quizzes"][0]   
         
    quiz_started = True
       
    score = score_quiz()
    return render_template('quiz.html', mainQuestion=question, data=data, length=len(data["quizzes"]), score=score)

@app.route('/results')
def quiz_results():
    score = score_quiz()
    if not score:
        return quiz(1)
    return render_template('quiz_results.html', score=score, data=data, length=len(data["quizzes"]))
    
def score_quiz():
    score = 0
    for question in data["quizzes"]:
        if question["attempts"] == 0:
            return None
        if question["option_chosen"] == question["answer"]:
            score += 1
    return score

@app.route('/quiz_answer/<int:quiz_num>', methods=['POST'])
def quiz_answer(quiz_num):
    question = data["quizzes"][quiz_num - 1]
    answer = int(request.json.get("answer"))
    
    if question["attempts"] < 2 and question["option_chosen"] != question["answer"]:
        question["attempts"] += 1
        question["option_chosen"] = answer
        correct = (answer == question["answer"])
        feedback = question["feedback"].get(answer, "Incorrect answer")

        if correct or question["attempts"] == 2:
            disable_submit = True
        else:
            disable_submit = False
    else:
        correct = (question["option_chosen"] == question["answer"])
        feedback = question["feedback"].get(question["option_chosen"], "Answer already selected")
        disable_submit = True

    return jsonify({"correct": correct, "feedback": feedback, "attempts": question["attempts"], "disable_submit": disable_submit})

@app.route('/retry_quiz')
def retryQuiz():
    resetQuiz()
    return quiz(1)

def resetQuiz():
    global quiz_started, quiz_answers
    quiz_started = False
    for question in data['quizzes']:
        question['option_chosen'] = None
        question['attempts'] = 0

# AJAX FUNCTIONS

if __name__ == '__main__':
    app.run(debug=True, port=5001)
