from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route('/')
def show_choices():
    return render_template('index.html', surveys=surveys)

@app.route('/start', methods=["POST"])
def show_start():
    survey_code = request.form["survey_choice"]

    session["survey_code"] = survey_code
    session["survey_length"] = len(surveys[survey_code].questions)
    print(session["survey_length"])

    survey = surveys[survey_code]
    return render_template('start.html', survey=survey)

@app.route('/start_survey', methods=["POST"])
def start_survey():
    session["responses"] = []
    session["comments"] = []

    return redirect(f'/question/0')

@app.route('/question/<int:q_num>')
def show_question(q_num):
    if len(session["responses"]) < session["survey_length"]:
        if int(q_num) == len(session["responses"]):
            question_obj = surveys[session["survey_code"]].questions[q_num]
            return render_template('question.html', q_num=q_num, question_obj=question_obj) 
        else:
            flash("You must answer survey questions in order", "error")
            return redirect(f'/question/{len(session["responses"])}')
    else:
        flash("You have already completed the survey", "error")
        return redirect('/thankyou')

@app.route('/answer', methods=["POST"])
def accept_answer():
    q_num = request.form["q_num"]
    answer = request.form["option"]
    comment = request.form.get("comment", None)

    response = session["responses"]
    response.append(answer)
    session["responses"] = response

    comments = session["comments"]
    comments.append(comment)
    session["comments"] = comments

    print(session)

    if int(q_num) < session["survey_length"] - 1:
        return redirect(f'/question/{int(q_num) + 1}')
    else: 
        return redirect('/thankyou')

@app.route('/thankyou')
def show_thanks():
    questions =  surveys[session["survey_code"]].questions
    return render_template('thankyou.html', questions=questions)
