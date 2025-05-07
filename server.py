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
        'link': 'https://www.youtube.com/watch?v=BpmMeIQywYc',
        'timestamp_no': 2,
        'timestamps': {
            26: 'The instruments only establish a consistent harmony. They never change their note, and the singer is the clear melody.',
            32: 'Other singers join in, but they sing the <em>exact same</em> melody — this is called <strong><u>homophony</u></strong>, which was used prominently in Medieval music.'
        }
    },
    2: {
        'genre': 'Medieval',
        'composer': 'Gregorian Chant',
        'piece': 'Deum vera',
        'link': 'https://www.youtube.com/watch?v=kK5AohCMX0U',
        'timestamp_no': 1,
        'timestamps': {
            0: 'Medieval music didn\'t always use instruments; notice there are only singers. But the texture is still <strong>homophonic</strong>.'
        }
    },
    3: {
        'genre': 'Renaissance',
        'composer': 'Josquin des Prez',
        'piece': 'Ave Maria',
        'link': 'https://www.youtube.com/watch?v=xGkb5KFwx1I',
        'timestamp_no': 2,
        'timestamps': {
            0: 'Notice the entrances - soprano, alto, tenor, finally bass. Their <em>staggered entrances</em> create a multi-line melodic figure.',
            15: 'This is known as <strong>polyphony</strong>, which differentiates Renaissance from Medieval music.'
        }
    },
    4: {
        'genre': 'Renaissance',
        'composer': 'Carlo Gesualdo',
        'piece': 'Moro Lasso',
        'link': 'https://www.youtube.com/watch?v=xGkb5KFwx1I',
        'timestamp_no': 2,
        'timestamps': {
            30: 'The voices move together, BUT they sing <em>different pitches</em>, creating more complex harmony.',
            40: 'Lyrics can have religious connotations (e.g., Dieu, Deus, etc.).'
        }
    },
    5: {
        'genre': 'Baroque',
        'composer': 'J.S. Bach',
        'piece': 'Harpsichord Concerto No. 1',
        'link': 'https://www.youtube.com/watch?v=XcsfDxojdV8',
        'timestamp_no': 2,
        'timestamps': {
            3: 'Instrumentations becomes more important; namely the <strong>harpsichord</strong> becomes the most famous instrument of this era.',
            15: 'The <strong>concerto</strong> starts becoming more popular, where a soloist is accompanied by an orchestra.'
        }
    },
    6: {
        'genre': 'Baroque',
        'composer': 'G.F. Handel',
        'piece': 'Julius Caesar, Act II',
        'link': 'https://www.youtube.com/watch?v=ppAUohisvG8',
        'timestamp_no': 2,
        'timestamps': {
            30: 'Notice how the violins and soprano sing melody, while the cello, bass, and harpsichord provide rhythmic and harmonic foundation.',
            48: 'They are known as the <strong>continuo</strong>, which is very representative of the Baroque era.'
        }
    },
    7: {
        'genre': 'Classical',
        'composer': 'W.A. Mozart',
        'piece': 'Impresario Overture',
        'link': 'https://www.youtube.com/watch?v=7vaBubCmhWA',
        'timestamp_no': 3,
        'timestamps': {
            6: 'Notice how loud and heroic we start.',
            10: "Now it's suddenly quieter and tip toe-y.",
            14: "We're <em>suddenly</em> loud again! This sudden change in volume is popular in this genre."
        }
    },
    8: {
        'genre': 'Classical',
        'composer': 'Chevalier de Saint-Georges',
        'piece': 'Violin Concerto in A Major',
        'link': 'https://www.youtube.com/watch?v=eQ1unCtX6K0',
        'timestamp_no': 2,
        'timestamps': {
            170: 'There are small sprinkles of virtuosity, like the occasional fast notes of the violin.',
            180: 'Performs finish their notes <strong>elegantly</strong>, which is very characteristic of the Classical era as well.'
        }
    },
    9: {
        'genre': 'Romantic',
        'composer': 'Anton von Bruckner',
        'piece': 'Symphony No. 7',
        'link': 'https://www.youtube.com/watch?v=dSGOaTuAesY&t=528s',
        'timestamp_no': 2,
        'timestamps': {
            773: 'The orchestration is now (basically) the same as the modern orchestra -- strings, winds, brass, and percussion instruments.',
            784: 'The texture is very <strong>thick</strong> here, which is also supremely characteristic of Romantic music.',
            800: 'Mind you, only violas, cellos, bass, and 2 horns play here.'
        }
    },
    10: {
        'genre': 'Romantic',
        'composer': 'Ludwig van Beethoven',
        'piece': 'Symphony No. 5',
        'link': 'https://www.youtube.com/watch?v=yKl4T5BnhOA',
        'timestamp_no': 4,
        'timestamps': {
            0: 'A classic piece -- we start very loud and strong here.',
            8: 'Now we are suddenly quiet again (Classical does this too, remember?).',
            14: 'But we get <strong>gradually</strong> louder now, until we are loud again.',
            18: 'This <strong>gradual</strong> change in volume is what makes Romantic music different from Classical.'
        }
    },
    11: {
        'genre': 'Modern/Contemporary',
        'composer': 'Igor Stravinsky',
        'piece': 'The Rite of Spring',
        'link': 'https://www.youtube.com/watch?v=EkwqPJZe8ms',
        'timestamp_no': 2,
        'timestamps': {
            1429: 'There is no clear harmony anymore (it doesn\'t sound pretty anymore), because <strong>traditional rules get thrown out</strong>.',
            1438: 'There is a <strong>wide range</strong> of volumes here. We started pretty soft, and now TWO timpanis and the whole orchestra play 11 notes together.'
        }
    },
    12: {
        'genre': 'Modern/Contemporary',
        'composer': 'Krzysztof Penderecki',
        'piece': 'Threnody to the Victims of Hiroshima',
        'link': 'https://www.youtube.com/watch?v=HilGthRhwP8',
        'timestamp_no': 2,
        'timestamps': {
            115: 'Instrumentation can also vary wildly. The last piece had a regular orchestra, this piece only calls for strings.',
            125: 'Normally, this music is intended to <strong>evoke a specific emotion</strong> or <strong>write about a specific event</strong> (such as the bombing of Hiroshima here).'
        }
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

    return jsonify({"correct": correct, "feedback": feedback, "attempts": question["attempts"], "disable_submit": disable_submit, "quiz_complete": (score_quiz() is not None)})

@app.route('/retry_quiz')
def retryQuiz():
    resetQuiz()
    return quiz(1)

@app.route('/quiz')
def quiz_redirect():
    return redirect(url_for('quiz', quiz_num=1))
    
def resetQuiz():
    global quiz_started, quiz_answers
    quiz_started = False
    for question in data['quizzes']:
        question['option_chosen'] = None
        question['attempts'] = 0

@app.route('/review_answers')
def review_answers():
    if score_quiz() is None:
        return redirect(url_for('quiz', quiz_num=1))
    return render_template(
        'review_answers.html',
        data=data,
        length=len(data["quizzes"])
    )


# AJAX FUNCTIONS

if __name__ == '__main__':
    app.run(debug=True, port=5001)
