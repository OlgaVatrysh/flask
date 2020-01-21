from flask import render_template, redirect, url_for, session, request
from app import app
from app.Users import Users
from app.Questions import Questions

from app import initDB 

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    users = Users(app.database_url, session)
    if request.method == 'POST':
        users.login(request.form['username'], request.form['password'])
        return redirect(url_for('index'))
    return render_template('index.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    if 'id' not in session:
        return redirect(url_for('index'))
    if 'answers' in session and session['answers'] != []:
        if session['answers'][-1]['question_id'] != question_id-1: 
            return redirect('/question/'+str(session['answers'][-1]['question_id']+1))
        for answers in session['answers']: 
            if int(answers['question_id']) == int(question_id): 
                return redirect('/question/'+str(session['answers'][-1]['question_id']+1)) 
    elif question_id != 1:
        return redirect(url_for('index'))
    questions = Questions(app.database_url, session)
    question = questions.getQuestion(question_id)
    if question == False:
        return redirect(url_for('finish'))
    if request.method == 'POST':
        questions.setAnswer(question_id, request.form)
        return redirect('/question/'+str(question_id+1))
    return render_template('question.html', question=question)

@app.route('/new')
def new():
    if 'answers' in session:
        session['answers'] = []
        session['next_question'] = 0
    return redirect('/question/1')

@app.route('/finish')
def finish():
    if 'id' not in session or 'answers' not in session or session['answers']==[]:
        return redirect(url_for('index'))
    questions = Questions(app.database_url, session)
    questions.setFinish()
    return render_template('finish.html')

@app.route('/result')
def result():
    if 'id' not in session:
        return redirect(url_for('index'))
    questions = Questions(app.database_url, session)    
    result = questions.getResults()
    return render_template('result.html', result=result)