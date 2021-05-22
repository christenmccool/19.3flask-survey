from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []

@app.route('/')
def show_survey_start():
    print(responses)
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/question/<int:q_num>')
def show_question(q_num):
    if len(responses) < len(satisfaction_survey.questions):
        if int(q_num) == len(responses):
            question_obj = satisfaction_survey.questions[q_num]
            return render_template('question.html', q_num=q_num, question_obj=question_obj) 
        else:
            flash("You must answer survey questions in order", "error")
            return redirect(f'/question/{len(responses)}')
    else:
        flash("You have already completed the survey", "error")
        return redirect('/thankyou')

@app.route('/answer', methods=["POST"])
def accept_answer():
    q_num = request.form["q_num"]
    answer = request.form["option"]
    responses.append(answer)
    if int(q_num) < len(satisfaction_survey.questions) - 1:
        return redirect(f'/question/{int(q_num) + 1}')
    else: 
        return redirect('/thankyou')

@app.route('/thankyou')
def show_thanks():
    return render_template('thankyou.html')
