from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "1234"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


responses_list = {}
answer_list = []


@app.route('/')
def _home():
    return render_template('home.html', surveys=survey)


@app.route('/', methods=["POST"])
def start_question():
    answer_list = []

    survey_key = request.form["survey_key"]
    print(survey_key)
    survey_to_take = survey[survey_key]
    responses_list["current_key"] = survey_key
    return render_template('pick_survey.html', survey=survey_to_take)


@app.route('/begin', methods=["POST"])
def begin():
    return redirect('/question/0')


@app.route('/question/<int:qid>')
def show_question(qid):

    survey_key = responses_list["current_key"]
    print(survey_key)

    len_response = len(answer_list)

    if len_response is None:
        return redirect('/')
    if len(survey[survey_key].questions) == len_response:
        return redirect('/complete')
    if len_response != qid:
        return redirect(f"/question/{len_response}")
    question = survey[survey_key].questions[qid]

    return render_template('question.html', question=question)

    # if len_response is None:
    #     return redirect('/')
    # if len_response == len(survey.questions):
    #     """ Answered all question"""
    #     return redirect('/complete')
    # if len_response != qid:
    #     """ trying to access question out of order"""
    #     return redirect(f"/question/{len_response}")
    # question = survey.questions[qid]
    # return render_template('question.html', question_num=qid, question=question)


@app.route('/answer', methods=["POST"])
def handle_answer():
    answer = request.args.get("answer")
    answer_list.append(answer)
    # if len(responses_list["cur_sur_ans"]) >= len(survey.questions):
    #     responses_list.clear()
    #     return redirect('/complete')
    # else:
    return redirect(f'/question/{len(answer_list)}')


@app.route('/complete')
def end_survey():
    return render_template("complete.html")
